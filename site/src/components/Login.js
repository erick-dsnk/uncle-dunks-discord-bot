import React from 'react';
import './Login.css';

class Login extends React.Component {
    render() {
        return (
            <div className="Login">
                <a
                    href="https://discord.com/api/oauth2/authorize?client_id=743859839821807736&redirect_uri=http%3A%2F%2Flocalhost%3A3000&response_type=token&scope=identify%20guilds"
                    className="loginButton"
                >Login with Discord</a>
            </div>
        );
    }
}

export default Login;