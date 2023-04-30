from channels import Group


def ws_connect(message):
    print("CONNECTING")
    Group('users').add(message.reply_channel)


def ws_disconnect(message):
    print("DISONECTING")
    Group('users').discard(message.reply_channel)
