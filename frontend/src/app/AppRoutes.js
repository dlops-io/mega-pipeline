import React from "react";
import { Route, Switch, Redirect } from 'react-router-dom';
import Home from "../components/Home";
import Delete from "../components/Delete";
import Error404 from '../components/Error/404';

const AppRouter = (props) => {

  console.log("================================== AppRouter ======================================");

  return (
    <React.Fragment>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/delete" exact component={Delete} />
        <Route component={Error404} />
      </Switch>
    </React.Fragment>
  );
}

export default AppRouter;