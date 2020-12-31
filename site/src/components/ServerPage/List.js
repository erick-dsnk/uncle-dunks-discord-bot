import React from 'react';
import Server from './Server';
import './List.css';

class List extends React.Component {
    render() {
        let guildList = [];

        for (let i = 0; i < this.props.guilds.length; i++) {
            let guildName = this.props.guilds[i].name;
            let guildId = this.props.guilds[i].id;

            guildList.push(
                <Server guildName={guildName} guildId={guildId} />
            )
        }

        return (
            <div className="List">
                <ul>
                    <>
                    {guildList}
                    </>
                </ul>
            </div>
        )
    }
}

export default List;