#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>SignUp</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        main_content = """
        <h1>Signup</h1>
        <form method="post" action="/success">
            <table>
                <tr>
                    <td>
                        Username
                    </td>
                    <td>
                        <input name="username">
                    </td>
                </tr>
                <tr>
                    <td>
                        Password
                    </td>
                    <td>
                        <input name="password" type="password">
                    </td>
                </tr>
                <tr>
                    <td>
                        Verify Password
                    </td>
                    <td>
                        <input name="vpassword" type="password">
                    </td>
                </tr>
                <tr>
                    <td>
                        Email (optional)
                    </td>
                    <td>
                        <input name="email">
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
        """

        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        response = page_header + main_content + error_element + page_footer

        self.response.write(response)

class Success(webapp2.RequestHandler):
    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        vpassword = self.request.get("vpassword")
        email = self.request.get("email")

        if not username:
            error = "Enter a username"
            self.redirect("/?error=" + error)

        if not valid_username(username):
            error = "Invalid username"
            self.redirect("/?error=" + error)

        if not password:
            error = "Enter a password"
            self.redirect("/?error=" + error)

        if not valid_password(password):
            error = "Invalid Password"
            self.redirect("/?error=" + error)

        if password != vpassword:
            error = "Passwords do not match"
            self.redirect("/?error=" + error)

        if email:
            if not valid_email(email):
                error = "Invalid email"
                self.redirect("/?error=" + error)

        response = "<h1>Welcome %s</h1>" % username
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/success', Success)
], debug=True)
