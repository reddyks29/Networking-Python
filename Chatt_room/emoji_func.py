def emoji_con(message):
    word=message.split(" ")
    emoji={
        ":)":"😊",
        ":(":":😌"
    }
    output=""
    for x in word:
        output+=emoji.get(x,x)+" "
    print(output)
message=input(">")
print(emoji_con(message))