def out():
    return Response(open("result.txt").read(),mimetype="text/txt")

out()
