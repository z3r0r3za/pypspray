# Pypspray
Python password spray

Specifically set up to work with Roundcube so far. It should work as long as the Roundcube config doesn't limit the number of login attempts. I might add the ability to do 3 passwords at a time for each username with a delay for rate limiting if I have time. Currently I only use it with one username at a time (one username in the file). To work with other email software it might have to be modified.

It is setup to work with a proxy through ZAP or Burp Suite so you should have one of those and a browser open and ready to go.

Usage: python3 url path_param un_file pw_file
Example: python3 pypspray "https://domain.com/mail" "/?_task=login" usernames.txt passwords.txt'

Give it a username file and a password file. It should loop through each username with the list of passwords.
