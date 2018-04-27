import json
import telepot
from django.http import (HttpResponseBadRequest,
                         JsonResponse)
# from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

# token = '264305012:AAFA2nbvNmTmuHX-CZlCtjJkHfKK-j9K9I2'
# tbot = telepot.Bot(token)
# translate, define, parse for dates

def _display_help():
    return render_to_string('help.md')


# CSRF Exempt for the POST requests from Telegram
@method_decorator(csrf_exempt, name='dispatch')
class CommandReceiveView(View):
    def __init__(self):
        self.token = '56430501:AAFA2nbvNmTmuHX-CZlCtjJkHfKK-j9K9I'
        self.telegram_bot = telepot.Bot(self.token)

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Hello World!")

    def post(self, request, *args, **kwargs):
        base_commands = {
            'help': _display_help,
            # '/define': _display_help,
        }

        raw = request.body.decode('utf-8')
        try:
            payload = json.loads(raw)
        except ValueError as e:
            print("error:", e)
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')
            func = base_commands.get(cmd.split()[0].lower())
            if func:
                self.telegram_bot.sendMessage(chat_id,
                                              func(),
                                              parse_mode='Markdown')
            else:
                pass
        return JsonResponse({}, status=200)
