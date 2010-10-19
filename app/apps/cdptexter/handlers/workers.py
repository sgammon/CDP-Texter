import twilio, logging, simplejson as json
from tipfy import RequestHandler, Response



class SendSMS(RequestHandler):
    
    def get(self):
        return Response('<b>Must POST to this worker</b>')
        
        
    def post(self):
        
        logging.info('Beginning new Twilio SMS worker...')

        logging.info('==== Debug Params ====')

        ### Pull some parameters out
        list_p = self.request.form.get('list')
        number = self.request.form.get('number')
        message = self.request.form.get('message')
        
        logging.info('list_p: '+str(list_p))
        logging.info('number: '+str(number))
        logging.info('message: '+str(message))

        logging.info('==== Twilio Info ====')

        ### Set things up on Twilio
        ACCOUNT_SID = 'AC8cb910ac2bc06ed184232be22bca8cf2'
        ACCOUNT_TOKEN = 'e3eddb2fcb7ba2f9c63f7390f6751626'
        CALLER_ID = '+14155992671'
        API_VERSION = '2010-04-01'

        logging.info('sid: '+str(ACCOUNT_SID))
        logging.info('token: '+str(ACCOUNT_TOKEN))
        logging.info('caller_id: '+str(CALLER_ID))
        logging.info('api_version: '+str(API_VERSION))

        account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN)
        
        d = {
            'From' : CALLER_ID,
            'To' : number,
            'Body' : message,
        }
        try:
            response = account.request('/%s/Accounts/%s/SMS/Messages.json' % \
                                      (API_VERSION, ACCOUNT_SID), 'POST', d)
                                  
            response_obj = json.loads(response)
        
            logging.info('TW Response: '+str(response))
            logging.info('SMS send successful.')
        
            return Response('<b>A-OK (Send Successful)</b>')
        except Exception, e:
            raise e