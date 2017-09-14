# -*- coding: UTF-8 -*-
from flask import Flask
from flask import request, jsonify
import datetime

app = Flask(__name__)

users_student = {}
users_instructor = {}
leave = {}


class ERROR:
    USER_NOT_FOUND = 400
    USER_ALREADY_EXIST = 401
    WRONG_PASSWORD = 402


class SUCCESS:
    REGISTER_SUCCESS = 200
    LOGIN_SUCCESS = 201
    askForLeave = 202


class DEAL:
    APPROVED = 301
    DISAPPROVED = 302


def result(code):
    return jsonify({'code': code})


class User:
    STUDENT = 1
    INSTRUCTOR = 2

    def __init__(self):
        self.number = None
        self.name = None
        self.password = None
        self.role = None
        self.links = []


class Leave:
    APPROVED = 1
    DISAPPROVED = 0

    def __init__(self):
        self.name = None
        self.number = None
        self.leave_time = None
        self.leave_reason = None
        self.approved = -1
        self.received_time = None

    def to_json(self):
        json_dict = dict()
        json_dict['name'] = self.name
        json_dict['number'] = self.number
        json_dict['leave_time'] = self.leave_time
        json_dict['leave_reason'] = self.leave_reason
        json_dict['received_time'] = self.received_time
        json_dict['approved'] = self.approved
        return jsonify(json_dict)

    def to_approved(self):
        self.approved = 1
        return self.approved

    def to_disapproved(self):
        self.approved = 0
        return self.approved


ymm = User()
ymm.number = '123456'
ymm.password = '123456'
ymm.role = User.INSTRUCTOR
ymm.links.append('41624101')
ymm.links.append('41624102')
users_instructor[ymm.number] = ymm

l = User()
l.name = '房轲'
l.number = '41624101'
l.password = '123456'
l.role = User.STUDENT
users_student[l.number] = l

lj = User()
lj.name = '连杰'
lj.number = '41624102'
lj.password = '123456'
lj.role = User.STUDENT
users_student[lj.number] = lj


# @app.route('/register', methods=['POST'])
# def register():
#     json = request.get_json()
#     number = json.get('number')
#     name = json.get('name')
#     class_name = json.get('class_name')
#     password = json.get('password')
#     role = json.get('role')
#
#     if role == User.STUDENT:
#         if number in users_student:
#             return result(ERROR.USER_ALREADY_EXIST)
#         else:
#             new_user = User()
#             new_user.number = number
#             new_user.name = name
#             new_user.class_name = class_name
#             new_user.password = password
#             users_student[number] = new_user
#             return result(SUCCESS.REGISTER_SUCCESS)
#
#     else:
#         if number in users_instructor:
#             return result(ERROR.USER_ALREADY_EXIST)
#         else:
#             new_user = User()
#             new_user.number = number
#             new_user.name = name
#             new_user.password = password
#             users_instructor[number] = new_user
#             return result(SUCCESS.REGISTER_SUCCESS)


@app.route('/login', methods=['POST'])
def login():
    json = request.get_json()
    number = json.get('number')
    password = json.get('password')
    role = json.get('role')
    if role == User.STUDENT:
        if number not in users_student:
            return result(ERROR.USER_NOT_FOUND)
        elif password != users_student[number].password:
            return result(ERROR.WRONG_PASSWORD)
        else:
            return result(SUCCESS.LOGIN_SUCCESS)

    else:
        if number not in users_instructor:
            return result(ERROR.USER_NOT_FOUND)
        elif password != users_instructor[number].password:
            return result(ERROR.WRONG_PASSWORD)
        else:
            return result(SUCCESS.LOGIN_SUCCESS)


@app.route('/student/AskForLeave', methods=['POST'])
def student_ask_for_leave():
    json = request.get_json()
    leave_time = json.get('leave_time')
    leave_reason = json.get('leave_reason')
    number = json.get('number')
    new_leave = Leave()
    new_leave.name = users_student[number].name
    new_leave.number = users_student[number].number
    new_leave.leave_time = leave_time
    new_leave.leave_reason = leave_reason
    new_leave.received_time = datetime.datetime.now()
    leave[number] = new_leave
    return result(SUCCESS.askForLeave)


@app.route('/student/GetResult', methods=['POST'])
def student_get_result():
    json = request.get_json()
    number = json.get('number')
    return leave[number].to_json()


@app.route('/instructor/GetPendingLeaves', methods=['POST'])
def instructor_get_pending_leaves():
    json = request.get_json()
    number = json.get('number')
    student_number_all = users_instructor[number].links

    leave_number = []
    for stu in student_number_all:
        if stu in leave:
            leave_number.append(stu)

    # for student_number in leave_number:  
    return leave[leave_number[0]].to_json()

    # leave_to_json = []
    # i = 0
    # for student_number in leave_number:
    #     leave_to_json.append(leave[student_number].to_json())
    #     i += 1


@app.route('/instructor/LeaveDeal', methods=['POST'])
def instructor_approve():
    json = request.get_json()
    number = json.get('number')
    approved = json.get('approved')
    student_number_all = users_instructor[number].links
    res = []
    for stu in student_number_all:
        if stu in leave:
            res.append(stu)
    student_number = res[0]
    if approved == Leave.APPROVED:
        leave[student_number].approved = Leave.APPROVED
        return result(DEAL.APPROVED)
    if approved == Leave.DISAPPROVED:
        leave[student_number].disapproved = Leave.DISAPPROVED
        return result(DEAL.DISAPPROVED)


if __name__ == '__main__':
    app.run("0.0.0.0")
