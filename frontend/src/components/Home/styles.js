
const styles = theme => ({
    root: {
        flexGrow: 1,
        minHeight: "100vh"
    },
    grow: {
        flexGrow: 1,
    },
    main: {

    },
    container: {
        backgroundColor: "#ffffff",
        paddingTop: "30px",
        paddingBottom: "20px",
    },
    recordingContainer: {
        // backgroundColor: "#333333",
        padding: "10px",
        marginLeft: "10px",
    },
    audioContainer: {
        textAlign: "center",
        padding: "10px",
    },
    buttonsContainer: {
        textAlign: "center",
        paddingTop: "10px",
    },
    startRecording: {
        color: "#de2d26",
        fontSize: "3.0rem",
        cursor: "pointer",
    },
    stopRecording: {
        color: "#ff0000",
        fontSize: "3.0rem",
        cursor: "pointer",
    },
    uploadRecording: {
        marginLeft: "20px",
        color: "#ffffff",
        fontSize: "3.0rem",
        cursor: "pointer",
    },
    textColumn: {
        width: "250px",
    },
    audioPlayer: {
        width: "150px",
        margin: "5px",
    },
    pavlos: {
        width: "60px",
    },
    group: {
        fontWeight: 800
    },
    cellItem: {
        paddingBottom: "5px",
    },
    showMoreBox: {
        borderRadius: "3px",
        backgroundColor: "#f0f0f0",
        border: "1px solid #ccc",
        padding: "8px",
    }
});

export default styles;