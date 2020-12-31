import React from 'react';
import './Server.css';


class Server extends React.Component {
    render() {

        return (
            <div className="Server">
                <h3>
                    <a href="">{this.props.guildName}</a>
                </h3>

                <br />

                <span>
                    Server ID: {this.props.guildId}
                </span>
            </div>
        )
    }
}

export default Server;