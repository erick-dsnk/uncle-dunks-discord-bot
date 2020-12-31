import React from 'react';
import './Servers.css';

import List from './List';

class Servers extends React.Component {
    render() {
        return (
            <div className="Servers">
                <h1>
                    Servers
                </h1>

                <List guilds={this.props.guilds} />
            </div>
        )
    }
}

export default Servers;