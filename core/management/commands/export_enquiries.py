import csv
from django.core.management.base import BaseCommand
from core.models import Enquiry


class Command(BaseCommand):
    help = 'Export enquiries to CSV (prints to stdout or writes to file when --output provided)'

    def add_arguments(self, parser):
        parser.add_argument('--output', '-o', help='Output file path (optional)')

    def handle(self, *args, **options):
        output = options.get('output')
        qs = Enquiry.objects.order_by('created_at')
        field_names = ['name', 'email', 'message', 'created_at']

        if output:
            f = open(output, 'w', newline='', encoding='utf-8')
        else:
            import sys
            f = sys.stdout

        writer = csv.writer(f)
        writer.writerow(field_names)
        for obj in qs:
            writer.writerow([getattr(obj, f) for f in field_names])

        if output:
            f.close()
            self.stdout.write(self.style.SUCCESS(f'Wrote {qs.count()} enquiries to {output}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Wrote {qs.count()} enquiries to stdout'))
