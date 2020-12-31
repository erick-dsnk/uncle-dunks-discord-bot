import React from 'react';

import Header from './Header';
import Servers from './ServerPage/Servers';
import Login from './Login';


class Dashboard extends React.Component {
    render() {

        return (
            <div className="Dashboard">
                {
                    this.props.data ? (
                        <Header
                            username={
                                this.props.data.profile.username
                            }
                            discriminator={
                                this.props.data.profile.discriminator
                            }
                        />
                    ) : (
                        <Header />
                    )
                }
                
                {
                    this.props.data ? (
                        <Servers guilds={this.props.data.guilds} />
                    ) : (
                        <Login />
                    )
                }
            </div>
        )
    }
}

export default Dashboard;