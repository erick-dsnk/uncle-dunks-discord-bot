import React from 'react';
import './Header.css';

class Header extends React.Component {
    render() {
        return (
            this.props.username ? (
                <div className="Header">
                    <h1 className="title"><a href="/">Uncle Dunk</a></h1>
                
                    <div className="navBar">
                        <span>
                            <strong>
                                {this.props.username}#{this.props.discriminator}
                            </strong>
                        </span>

                        <a href="/invite" className="navLink">
                            <strong>Invite</strong>
                        </a>
                    </div>
                </div>
            ) : (
                <div className="Header">
                    <h1 className="title"><a href="/">Uncle Dunk</a></h1>
                
                    <div className="navBar">
                        <a href="/invite" className="navLink">
                            <strong>Invite</strong>
                        </a>
                    </div>
                </div>
            )
            
        );
    }
    
}

export default Header;