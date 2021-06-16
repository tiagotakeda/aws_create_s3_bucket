import pexpect
import sys

child = pexpect.spawn('py t.py')
child.expect('Password: ')
child.sendline('1234')
child.interact()