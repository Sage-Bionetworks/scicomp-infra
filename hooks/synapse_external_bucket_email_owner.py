import logging

from sceptre.hooks import Hook
from botocore.exceptions import ClientError

"""
The purpose of this hook is to run additional setup after creating
a Synapse external bucket.  For more information please refer to the
[synapse external bucket documention](http://docs.synapse.org/articles/custom_storage_location.html)

Does the following after creation of the bucket:
* Send an email to the bucket owner with the bucket info.

Example:

    template_path: templates/SynapseExternalBucket.yaml
    stack_name: GatesKI-TestStudy
    hooks:
      after_create:
        - !synapse_external_bucket_email_owner

"""
class SynapseExternalBucketEmailOwner(Hook):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self, *args, **kwargs):
        super(SynapseExternalBucketEmailOwner, self).__init__(*args, **kwargs)

    def run(self):
        """
        run is the method called by Sceptre. It should carry out the work
        intended by this hook.
        """
        region = self.environment_config['region']
        stack_name = self.stack_config['stack_name']

        # Therefore we need to get parameter values from cloudformation
        response = self.request_cf_decribe_stacks(stack_name)
        stack_parameters = response['Stacks'][0]['Parameters']
        stack_outputs = response['Stacks'][0]['Outputs']
        owner_email = self.get_parameter_value(stack_parameters, 'OwnerEmail')
        synapse_bucket = self.get_output_value(stack_outputs,
                                               region + '-' + stack_name + '-' + 'SynapseExternalBucket')
        self.logger.debug("Synapse external bucket name: " +  synapse_bucket)

        self.email_owner(owner_email, synapse_bucket)


    def email_owner(self, owner_email, synapse_bucket):
        client = self.connection_manager.boto_session.client('ses')

        # This address must be verified with Amazon SES.
        SENDER = "AWS Scicomp <aws.scicomp@sagebase.org>"

        # if SES is still in the sandbox, this address must be verified.
        RECIPIENT = owner_email

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        # CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        # AWS_REGION = "us-west-2"

        # The subject line for the email.
        SUBJECT = "Scicomp Automated Provisioning"

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("An S3 bucket has been provisioned on your behalf. "
                     "The bucket name is " + synapse_bucket)

        # The HTML body of the email.
        BODY_HTML1 = """<html>
        <head></head>
        <body>
          <p>"""
        BODY_HTML2 = """</p>
        </body>
        </html>
        """

        # The character encoding for the email.
        CHARSET = "UTF-8"

        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML1 + BODY_TEXT + BODY_HTML2,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        except ClientError as e:
            self.logger.error(e.response['Error']['Message'])
        else:
            self.logger.info("Email sent to " + RECIPIENT)
            self.logger.info("Message ID: " + response['MessageId'])


class UndefinedExportException(Exception):
    pass


class UndefinedParameterException(Exception):
    pass
