[![Tools](https://skillicons.dev/icons?i=python,django)](https://skillicons.dev)
<h1>User A Django Web Application.</h1>
<p>This application provides a <b>custom user authentication model</b> (Account), a <b>user information model</b> (Profile), <b>logger</b> and <b>super user actions</b>.</p>
<h1>To Use This Application.</h1>
<ol>
    <li>Install all requirements in <b>requirement.txt</b> file.</li>
    <li>You can't have another app under tha name <b>'user'</b>.</li>
    <li>Include the app in the <b>INSTALLED_APPS</b> as <b>'user.apps.UserConfig'</b>.</li>
    <li>Set <b>AUTH_USER_MODEL</b> to <b>'user.Account'</b>.</li>
</ol>
<hr>
<table>
    <tr>
        <th>Sign</th>
        <td>A user uses this template to access sign forms (signup and signin), also it contains a descriptive paragraph.</td>
    </tr>
    <tr>
        <th>Settings</th>
        <td>A user uses this template to view and update his account data, (update profile picture and information, update account password).</td>
    </tr>
    <tr>
        <th>Panel</th>
        <td>A user (super-user) uses this template to list users, view each user's log, deactivating/activating users and deleting users.</td>
    </tr>
</table>