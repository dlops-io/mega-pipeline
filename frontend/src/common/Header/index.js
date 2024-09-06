import React from 'react';
import { withStyles } from '@material-ui/core';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import { Link } from 'react-router-dom';


import styles from './styles';

const Header = (props) => {
    const { classes } = props;

    console.log("================================== Header ======================================");

    return (
        <div className={classes.root}>
            <AppBar position="static" elevation={0}>
                <Toolbar variant="dense">
                    <IconButton className={classes.menuButton} color="inherit" aria-label="Menu">
                        <MenuIcon />
                    </IconButton>
                    <Link to="/" className={classes.appLink}>
                        <Typography className={classes.appTitle} >
                            AC215: Mega Pipeline App
                        </Typography>
                    </Link>

                    <div className={classes.grow} />

                </Toolbar>
            </AppBar>
        </div>
    );
}

export default withStyles(styles)(Header);
