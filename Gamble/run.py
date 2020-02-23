from config import users, original_budget, budget_history, current_budget, user_hosts

'''
from flask import Flask, request, render_template
from flask_cors import CORS
import json
'''

app = Flask(__name__)
CORS(app=app)

user_host = {
}

@app.route('/', methods=['GET'])
def coin_status():
    str_ver = '<h1>누가 얼마나 가졌나볼까요!</h1>'

    for user in current_budget:
        str_ver += f"<h1>{user}: {current_budget[user]} 원 << {original_budget[user]}</h1>"
    rtn_val = f"""
<!DOCTYPE HTML>
<html>
    {str_ver}
</html>
"""
    return rtn_val


@app.route('/등록/<username>', methods=['GET'])
def register(username):
    global user_host
    
    if username not in original_budget:
        user_list = str(list(original_budget.keys())).replace(',', ' ').replace('\'', '').replace('[', '').replace(']', '')
        str_ver = f"<h1>{username} 가 누구죠? 유저리스트에 없는데...</h1><h1> 가능한 유저들: {user_list}</h1>"
    else:
        remote_host = request.environ['REMOTE_ADDR']
        user_host[remote_host] = username
        str_ver = f"<h1>{username} 에 당신의 호스트를 ({remote_host}) 연결했습니다!</h1>"
    rtn_val = f"""
<!DOCTYPE HTML>
<html>
    {str_ver}
</html>
"""

    return rtn_val


@app.route('/<to_user>/<amount>', methods=['GET'])
def send_coin(to_user, amount):
    global current_budget

    if to_user not in current_budget:
        user_list = str(list(current_budget.keys())).replace(',', ' ').replace('\'', '').replace('[', '').replace(']', '')
        str_ver = f"<h1>{to_user} 가 누구죠? 유저리스트에 없는데...</h1><h1> 가능한 유저들: {user_list}</h1>"
    else:
        remote_host = request.environ['REMOTE_ADDR']

        if remote_host not in user_host:
            str_ver = f"<h1>누구세요? 호스트 IP 가 처음보는 주소인데... 등록은 하셨나요?</h1>"
        else:
            from_user = user_host[remote_host]
            current_budget[from_user] -= int(amount)
            current_budget[to_user] += int(amount)
            str_ver = f"<h1>{from_user}가 {to_user}에게 {amount}원을 보냅니다!</h1><h1>남은 돈:</h1><h1>{from_user}: {current_budget[from_user]}</h1><h1>{to_user}: {current_budget[to_user]}</h1>"

    rtn_val = f"""
<!DOCTYPE HTML>
<html>
    {str_ver}
</html>
"""
    return rtn_val

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
