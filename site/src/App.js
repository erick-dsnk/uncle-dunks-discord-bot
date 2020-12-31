import './App.css';

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import axios from 'axios';

import Dashboard from './components/Dashboard';

import { getCodeFromUri } from './discord';


function App() {
  const returnValues = getCodeFromUri();

  let accessToken = returnValues.accessToken;
  let tokenType = returnValues.tokenType;

  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      let resultData = {};

      const profileResult = await axios(
        'https://discord.com/api/users/@me',
        {
          headers: {
            authorization: `${tokenType} ${accessToken}`
          }
        }
      );

      resultData['profile'] = profileResult.data;

      const guildsResult = await axios(
        'https://discord.com/api/users/@me/guilds',
        {
          headers: {
            authorization: `${tokenType} ${accessToken}`
          }
        }
      );

      resultData['guilds'] = guildsResult.data;

      let guilds = [];

      for (let i=0; i < resultData.guilds.length; i++) {
        let guildId = resultData.guilds[i].id;
        let guildPerms = resultData.guilds[i].permissions;

        if ((guildPerms & 20) === 20) {
          guilds.push(resultData.guilds[i]);
        }
      }

      resultData['guilds'] = guilds;

      setData(resultData);
    };

    fetchData();
  });

  console.log(data);
  
  return (
  
    <Router>
      <div className="App">
        <Route path="/" component={
          () => <Dashboard data={data} />
        } exact />
      </div>
    </Router>
  );
}

export default App;
