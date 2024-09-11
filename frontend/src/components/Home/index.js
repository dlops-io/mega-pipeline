import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
// import MicRecorder from 'mic-recorder-to-mp3';
import Icon from '@material-ui/core/Icon';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Toolbar from '@material-ui/core/Toolbar';
import Divider from '@material-ui/core/Divider';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ShowMoreText from "react-show-more-text";


import DataService from "../../services/DataService";
import { BASE_API_URL } from "../../services/Common";
import styles from './styles';

// const recorder = new MicRecorder({
//     bitRate: 128
// });

const Home = (props) => {
    const { classes } = props;

    console.log("================================== Home ======================================");


    // Component States
    const [isRecording, setIsRecording] = useState(false);
    const [blobURL, setBlobURL] = useState(null);
    const [isBlocked, setIsBlocked] = useState(true); // Set true or false to disable mic
    const [audioBlob, setAudioBlob] = useState(null);
    const [inputAudios, setInputAudios] = useState([]);
    const loadInputAudios = () => {
        DataService.GetInputAudios()
            .then(function (response) {
                console.log(response.data);
                setInputAudios(response.data);
            })
    }
    const [expand1, setExpand1] = useState(false);
    const [expand2, setExpand2] = useState(false);
    const [expand3, setExpand3] = useState(false);


    // Setup Component
    useEffect(() => {
        loadInputAudios();
    }, []);
    //Get permission from user to use mic
    try {
        navigator.mediaDevices.getUserMedia({ audio: true },
            () => {
                console.log('Permission Granted');
                setIsBlocked(false);
            },
            () => {
                console.log('Permission Denied');
                setIsBlocked(true);
            },
        );
    }
    catch (err) {
        //setIsBlocked(true);
        console.log('Could not get navigator.mediaDevices.getUserMedia');
        console.log(err.message);
    }


    // Handlers
    const handleOnStartRecording = () => {
        if (isBlocked) {
            console.log('Permission Denied');
        } else {
            // recorder
            //     .start()
            //     .then(() => {
            //         setIsRecording(true);
            //     })
            //     .catch((e) => console.error(e));
        }
    }
    const handleOnStopRecording = () => {
        // recorder
        //     .stop()
        //     .getMp3()
        //     .then(([buffer, blob]) => {
        //         setBlobURL(URL.createObjectURL(blob));
        //         setIsRecording(false);
        //         setAudioBlob(blob);

        //         var formData = new FormData();
        //         formData.append("file", blob);
        //         DataService.SaveAudio(formData)
        //             .then(function (response) {
        //                 console.log(response.data);
        //                 setInputAudios([]);
        //                 loadInputAudios();
        //             })

        //     }).catch((e) => console.log(e));
    }

    function useInterval(callback, delay) {
        const savedCallback = useRef();

        // Remember the latest function.
        useEffect(() => {
            savedCallback.current = callback;
        }, [callback]);

        // Set up the interval.
        useEffect(() => {
            function tick() {
                savedCallback.current();
            }
            if (delay !== null) {
                let id = setInterval(tick, delay);
                return () => clearInterval(id);
            }
        }, [callback, delay]);
    }
    function showMoreClick1() {
        setExpand1(!expand1)
    }
    function showMoreClick2() {
        setExpand2(!expand2)
    }
    function showMoreClick3() {
        setExpand3(!expand3)
    }

    useInterval(async () => {
        loadInputAudios();
    }, 10000)

    const showMore = <span className={classes.showMoreButton}>&nbsp; show more</span>
    const showLess = <span className={classes.showMoreButton}>&nbsp; show less</span>


    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Container maxWidth={false} className={classes.container}>
                    {!isBlocked &&
                        <Toolbar className={classes.toolBar}>
                            <Typography>
                                Click mic to record a Prompt:
                            </Typography>
                            <div className={classes.recordingContainer}>
                                {/* <span className={classes.audioContainer}>
                                <audio src={blobURL} controls="controls" />
                            </span> */}
                                <span className={classes.buttonsContainer}>
                                    {!isRecording &&
                                        <Icon className={classes.startRecording} onClick={() => handleOnStartRecording()}>mic</Icon>
                                    }
                                    {isRecording &&
                                        <Icon className={classes.stopRecording} onClick={() => handleOnStopRecording()}>stop_circle</Icon>
                                    }
                                </span>
                            </div>
                            <div className={classes.grow} />
                        </Toolbar>
                    }

                    {/* <Stepper activeStep={-1}>
                        <Step>
                            <StepLabel><Typography variant="h4">🎙️</Typography><Typography variant="caption">Record Prompt</Typography></StepLabel>
                        </Step>
                        <Step>
                            <StepLabel><Typography variant="h4">📝</Typography><Typography variant="caption">Transcribe Audio</Typography></StepLabel>
                        </Step>
                        <Step>
                            <StepLabel><Typography variant="h4">🗒️</Typography><Typography variant="caption">Generate Text</Typography></StepLabel>
                        </Step>
                        <Step>
                            <StepLabel><Typography variant="h4">🇫🇷</Typography><Typography variant="caption">Translate Text</Typography></StepLabel>
                        </Step>
                        <Step>
                            <StepLabel><Typography variant="h4">🔊</Typography><Typography variant="caption">Synthesis Audio</Typography></StepLabel>
                        </Step>
                    </Stepper> */}
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell align={'center'}>
                                        <Step>
                                            <StepLabel><Typography variant="h4">🎙️</Typography><Typography variant="caption">Audio Prompts</Typography></StepLabel>
                                        </Step>

                                    </TableCell>
                                    <TableCell align={'center'} className={classes.textColumn}>
                                        <Step>
                                            <StepLabel><Typography variant="h4">📝</Typography><Typography variant="caption">Transcribed Audio</Typography></StepLabel>
                                        </Step>
                                    </TableCell>
                                    <TableCell align={'center'}>
                                        <Step>
                                            <StepLabel><Typography variant="h4">🗒️</Typography><Typography variant="caption">Generated Text</Typography></StepLabel>
                                        </Step>
                                    </TableCell>
                                    <TableCell align={'center'}>
                                        <Step>
                                            <StepLabel><Typography variant="h4">🔊</Typography><Typography variant="caption">Synthesised Audio</Typography></StepLabel>
                                        </Step>
                                    </TableCell>
                                    <TableCell align={'center'}>
                                        <Step>
                                            <StepLabel><Typography variant="h4">🇫🇷</Typography><Typography variant="caption">Translated Text</Typography></StepLabel>
                                        </Step>
                                    </TableCell>
                                    <TableCell align={'center'}>
                                        <Step>
                                            <StepLabel><Typography variant="h4">🔊</Typography><Typography variant="caption">Synthesised Audio</Typography></StepLabel>
                                        </Step>
                                    </TableCell>
                                    <TableCell align={'center'}>
                                        <Step>
                                            <StepLabel>
                                                <img src='pavlos.png' className={classes.pavlos}></img>
                                            </StepLabel>
                                        </Step>
                                    </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {inputAudios && inputAudios.map((item, idx) =>
                                    <TableRow key={idx}>
                                        <TableCell>
                                            <audio controls className={classes.audioPlayer}>
                                                <source src={BASE_API_URL + "/get_audio_data?path=" + item.input_audio} type="audio/mp3" />
                                                Your browser does not support the audio element.
                                            </audio>
                                        </TableCell>
                                        <TableCell onClick={() => showMoreClick1()}>
                                            {item.text_prompts && item.text_prompts.map((sub_item, sub_idx) =>
                                                <div className={classes.cellItem} key={sub_idx}>
                                                    <div className={classes.group}>Group: {sub_item.group_name}</div>
                                                    <ShowMoreText
                                                        lines={3}
                                                        more={showMore}
                                                        less={showLess}
                                                        anchorClass="show-more-less-clickable"
                                                        expanded={expand1}
                                                        width={300}
                                                        truncatedEndingComponent={"... "}
                                                        className={classes.showMoreBox}
                                                    >
                                                        {sub_item.text_prompt}
                                                    </ShowMoreText>
                                                </div>
                                            )}

                                        </TableCell>
                                        <TableCell onClick={() => showMoreClick2()}>
                                            {item.text_prompts && item.text_paragraphs.map((sub_item, sub_idx) =>
                                                <div className={classes.cellItem} key={sub_idx}>
                                                    <div className={classes.group}>Group: {sub_item.group_name}</div>
                                                    <ShowMoreText
                                                        lines={3}
                                                        more={showMore}
                                                        less={showLess}
                                                        className={classes.showMoreBox}
                                                        anchorClass="show-more-less-clickable"
                                                        expanded={expand1}
                                                        width={300}
                                                        truncatedEndingComponent={"... "}
                                                    >
                                                        {sub_item.text_paragraph}
                                                    </ShowMoreText>
                                                </div>
                                            )}
                                        </TableCell>
                                        <TableCell>
                                            {item.text_audios && item.text_audios.map((sub_item, sub_idx) =>
                                                <div className={classes.cellItem} key={sub_idx}>
                                                    <div className={classes.group}>Group:{sub_item.group_name}</div>
                                                    <audio controls className={classes.audioPlayer}>
                                                        <source src={BASE_API_URL + "/get_audio_data?path=" + sub_item.text_audio} type="audio/mp3" />
                                                        Your browser does not support the audio element.
                                                    </audio>
                                                </div>
                                            )}
                                        </TableCell>
                                        <TableCell onClick={() => showMoreClick3()}>
                                            {item.text_translates && item.text_translates.map((sub_item, sub_idx) =>
                                                <div className={classes.cellItem} key={sub_idx}>
                                                    <div className={classes.group}>Group: {sub_item.group_name}</div>
                                                    <ShowMoreText
                                                        lines={3}
                                                        more={showMore}
                                                        less={showLess}
                                                        className={classes.showMoreBox}
                                                        anchorClass="show-more-less-clickable"
                                                        expanded={expand1}
                                                        width={300}
                                                        truncatedEndingComponent={"... "}
                                                    >
                                                        {sub_item.text_translate}
                                                    </ShowMoreText>
                                                </div>
                                            )}
                                        </TableCell>
                                        <TableCell>
                                            {item.output_audios && item.output_audios.map((sub_item, sub_idx) =>
                                                <div className={classes.cellItem} key={sub_idx}>
                                                    <div className={classes.group}>Group:{sub_item.group_name}</div>
                                                    <audio controls className={classes.audioPlayer}>
                                                        <source src={BASE_API_URL + "/get_audio_data?path=" + sub_item.output_audio} type="audio/mp3" />
                                                        Your browser does not support the audio element.
                                                    </audio>
                                                </div>
                                            )}
                                        </TableCell>
                                        <TableCell>
                                            {item.output_audios_pp && item.output_audios_pp.map((sub_item, sub_idx) =>
                                                <div className={classes.cellItem} key={sub_idx}>
                                                    <div className={classes.group}>Group:{sub_item.group_name}</div>
                                                    <audio controls className={classes.audioPlayer}>
                                                        <source src={BASE_API_URL + "/get_audio_data?path=" + sub_item.output_audio} type="audio/mp3" />
                                                        Your browser does not support the audio element.
                                                    </audio>
                                                </div>
                                            )}
                                        </TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Container>
            </main>
        </div>
    );
};

export default withStyles(styles)(Home);