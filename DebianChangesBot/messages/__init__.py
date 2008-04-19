
class Message(object):

    def format_email_address(self, email):
        email = re.sub(r'(?:<([-A-Za-z0-9]+)@debian.org>)', r'(\1)', email)
        email = re.sub(r'@(.{6}).*>', r'@\1..>', email)
        return email.replace(r'"', '')
