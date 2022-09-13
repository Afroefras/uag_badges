from os import system
from pathlib import Path
from getpass import getpass
from imaplib import IMAP4_SSL
from email import message_from_bytes

class GetEmailData:
    def __init__(self, username: str, date_from: str, date_to: str, domain: str='@edu.uag.mx', server: str='outlook.office365.com') -> None:
        '''
        use your email provider's IMAP server, you can look for your provider's IMAP server on Google
        or check this page: https://www.systoolsgroup.com/imap/
        for office 365, it's outlook.office365.com
        '''
        self.username = username
        self.domain = domain
        self.user_email = self.username + self.domain
        self.server = server
        self.date_from = date_from
        self.date_to = date_to


    def login(self) -> None: 
        password = getpass('Contraseña:\n')
        system('clear')
        self.imap = IMAP4_SSL(self.server)
        self.imap.login(self.user_email, password)


    def get_folders(self) -> list:
        all_folders = self.imap.list()[-1]
        all_folders = [x.decode('utf-8') for x in all_folders]
        all_folders = [x.split()[-1] for x in all_folders]
        return all_folders


    def filter_msg_dates(self, filter_from: str) -> None:
        self.imap.select(filter_from)
        to_filter = f'(SINCE "{self.date_from}" BEFORE "{self.date_to}")'
        _, filter_uids = self.imap.uid('search', None, to_filter)
        self.uids = filter_uids[0].split()
        self.uids = set(self.uids)
        

    def create_files_dir(self, create_user_folder: bool) -> None:
        base_dir = Path().cwd()
        if create_user_folder:
            base_dir = base_dir.joinpath(self.username)
            base_dir.mkdir(exist_ok=True)

        sub_dir_name = f'{self.date_from} to {self.date_to}'
        self.files_dir = base_dir.joinpath(sub_dir_name)
        self.files_dir.mkdir(exist_ok=True)


    def get_files(self) -> None:
        self.files_list = []
        for i, uid in enumerate(self.uids):
            new_id = str(i).zfill(3)
            _, data = self.imap.uid('fetch', uid, '(RFC822)')
            message_parts = message_from_bytes(data[0][1])

            if message_parts.get_content_maintype() == 'multipart':
                for msg_part in message_parts.walk():
                    #find the attachment part
                    if msg_part.get_content_maintype() == 'multipart': continue
                    if msg_part.get('Content-Disposition') is None: continue

                    filename = new_id
                    filename += msg_part.get_filename()
                    file_dir = self.files_dir.joinpath(filename)
                    
                    self.files_list.append({
                        'id': new_id,
                        'date': message_parts['date'],
                        'from': message_parts['from'],
                        'subject': message_parts['subject'],
                        'filename': filename,
                        'file_dir': file_dir,
                    })

                    with open(file_dir, 'wb') as f:
                        f.write(msg_part.get_payload(decode=True))

    def finish_session(self) -> None:
        self.imap.close()
        self.imap.logout()