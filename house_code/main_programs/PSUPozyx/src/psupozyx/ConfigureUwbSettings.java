package psupozyx;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.ChoiceBox;

public class ConfigureUwbSettings {
    @FXML
    private ChoiceBox m_channel;
    @FXML
    private ChoiceBox m_bitrate;
    @FXML
    private ChoiceBox m_prf;
    @FXML
    private ChoiceBox m_plen;
    @FXML
    private ChoiceBox m_gain;


    private int channel;
    private int bitrate;
    private int prf;
    private int plen;
    private float gain;


    public void handleLaunchConfigureUwb(ActionEvent actionEvent) {
    }

    public void handleMaximumRange(ActionEvent actionEvent) {
    }

    public void handleFavorRange(ActionEvent actionEvent) {
    }

    public void handleBalanced(ActionEvent actionEvent) {
    }

    public void handleFavorDataRate(ActionEvent actionEvent) {
    }

    public void handleMaximumDataRate(ActionEvent actionEvent) {
    }

    public void handleLaunchRanging(ActionEvent actionEvent) {
    }

    public void handleLaunchPositioning(ActionEvent actionEvent) {
    }

    public void handleLaunchMotionData(ActionEvent actionEvent) {
    }

    public void handleLaunchPositioningAndMotionData(ActionEvent actionEvent) {
    }

    public void handleQuit(ActionEvent actionEvent) {
        Platform.exit();
    }
}
