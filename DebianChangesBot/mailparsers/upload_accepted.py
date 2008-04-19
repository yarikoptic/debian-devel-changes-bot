
from DebianChangesBot import MailParser
from DebianChangesBot.formatters import UploadAcceptedFormatter

class BugSubmittedParser(MailParser):

    def parse(self, headers, body):

        fmt = UploadAcceptedFormatter()

        mapping = {
            'Source': 'package',
            'Version': 'version',
            'Distribution': 'distribution',
            'Urgency': 'urgency',
            'Changed-By': 'by',
            'Closes': 'closes',
        }

        for line in body:
            for field, target in mapping.iteritems():
                if line.startswith('%s: ' % field):
                    val = line[len(field) + 2:]
                    setattr(fmt, target, val)
                    del mapping[field]
                    break

            # If we have found all the field, stop looking
            if len(mapping) == 0:
                break

        return fmt
