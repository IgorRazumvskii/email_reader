from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmailAccount, Email
from .serializers import EmailAccountSerializer, EmailSerializer
import imaplib
import email
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class FetchEmailsView(APIView):
    def get(self, request):
        return render(request, 'mail/mail.html')

    def post(self, request, *args, **kwargs):
        email_account = get_object_or_404(EmailAccount, email=request.data.get('email'))
        password = email_account.password

        # Подключение к почтовому серверу
        mail = imaplib.IMAP4_SSL('imap.yandex.ru')
        mail.login(email_account.email, password)
        mail.select('inbox')

        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        emails = []

        # Поиск последнего импортированного сообщения
        last_email = Email.objects.filter(account=email_account).order_by('-received_date').first()
        last_email_id = last_email.id if last_email else None

        for idx, e_id in enumerate(email_ids):
            if e_id == last_email_id:
                break

            result, msg_data = mail.fetch(e_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            email_data = {
                'account': email_account.id,
                'subject': msg['subject'],
                'send_date': msg['date'],
                'received_date': msg['date'],
                'body': msg.get_payload(),
                'attachments': []
            }

            serializer = EmailSerializer(data=email_data)
            if serializer.is_valid():
                serializer.save()
                emails.append(serializer.data)

            # Обновление прогресс-бара
            progress = int((idx + 1) / len(email_ids) * 100)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'email_fetch_group',
                {
                    'type': 'update_progress',
                    'message': f'Чтение сообщений: {progress}% завершено'
                }
            )

        return Response(emails, status=status.HTTP_200_OK)

