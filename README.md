# Pypspray
Python password spray

This is a work in progress, but it works with Roundcube, if the Roundcube config doesn't limited the number of login attempts. It would have to be modified to work with some other email software. I might add the ability to do 3 passwords at a time for each username with a delay for rate limiting. I usually use it with one username at a time.

It is setup to work with a proxy through ZAP or Burp Suite so you should have one of those and a browser open and ready.

Usage: python3 url path_param un_file pw_file
Example: python3 pypspray "https://domain.com/mail" "/?_task=login" usernames.txt passwords.txt'

Give it a username file and a password file. It should loop through each username with the list of passwords.
