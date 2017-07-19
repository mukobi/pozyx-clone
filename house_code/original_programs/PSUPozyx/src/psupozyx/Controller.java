package psupozyx;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import java.io.*;
import java.util.Properties;

public class Controller {
    @FXML
    private GridPane grid_pane_stage;
    private Stage stage = (Stage) (grid_pane_stage != null ? grid_pane_stage.getScene().getWindow() : null);

    @FXML
    private Label m_status_display;
    // interface fields
    @FXML
    private CheckBox m_use_mobile_device;
    @FXML
    private TextField m_mobile_device_id;

    @FXML
    private TextField m_a1_id;
    @FXML
    private TextField m_a1_x;
    @FXML
    private TextField m_a1_y;
    @FXML
    private TextField m_a1_z;
    @FXML
    private TextField m_a2_id;
    @FXML
    private TextField m_a2_x;
    @FXML
    private TextField m_a2_y;
    @FXML
    private TextField m_a2_z;
    @FXML
    private TextField m_a3_id;
    @FXML
    private TextField m_a3_x;
    @FXML
    private TextField m_a3_y;
    @FXML
    private TextField m_a3_z;
    @FXML
    private TextField m_a4_id;
    @FXML
    private TextField m_a4_x;
    @FXML
    private TextField m_a4_y;
    @FXML
    private TextField m_a4_z;

    @FXML
    private CheckBox m_log_pressure;
    @FXML
    private CheckBox m_log_acceleration;
    @FXML
    private CheckBox m_log_magnetic;
    @FXML
    private CheckBox m_log_angular_velocity;
    @FXML
    private CheckBox m_log_euler_angles;
    @FXML
    private CheckBox m_log_quaternion;
    @FXML
    private CheckBox m_log_linear_acceleration;
    @FXML
    private CheckBox m_log_gravity;

    @FXML
    private CheckBox m_use_file;
    @FXML
    private TextField m_filename;
    @FXML
    private RadioButton m_use_txt_ext;

    @FXML
    private CheckBox m_use_processing;

    // field data variables
    private String use_remote;
    private String remote_id;
    private String anchor1_id;
    private String anchor1_x;
    private String anchor1_y;
    private String anchor1_z;
    private String anchor2_id;
    private String anchor2_x;
    private String anchor2_y;
    private String anchor2_z;
    private String anchor3_id;
    private String anchor3_x;
    private String anchor3_y;
    private String anchor3_z;
    private String anchor4_id;
    private String anchor4_x;
    private String anchor4_y;
    private String anchor4_z;

    private String log_pressure;
    private String log_acceleration;
    private String log_magnetic;
    private String log_angular_velocity;
    private String log_euler_angles;
    private String log_quaternion;
    private String log_linear_acceleration;
    private String log_gravity;

    private String use_file;
    private String filename;
    private String use_txt_ext;
    private String use_processing;


    @FXML
    private void handleLoadButtonAction(ActionEvent event) {
        update_variables_from_gui();
        FileChooser fileChooser = new FileChooser();
        configureFileChooser(fileChooser);
        File loadFile = fileChooser.showOpenDialog(stage);
        if (loadFile != null) {
            String templatePath = loadFile.getAbsolutePath();
            load_properties_from_file(templatePath);
        }
    }



    @FXML
    private void handleSaveTemplateButtonAction(ActionEvent event) {
        update_variables_from_gui();

        FileChooser fileChooser = new FileChooser();
        configureFileChooser(fileChooser);
        File templateFile = fileChooser.showSaveDialog(stage);
        if (templateFile != null) {
            String templatePath = templateFile.getAbsolutePath();
            save_properties_to_file(templatePath);
            m_status_display.setText("Successfully saved settings to template.");
        }

    }

    @FXML
    private void handleSaveUseButtonAction(ActionEvent event) {
        update_variables_from_gui();
        save_properties_to_file("Configurations/master_config_for_python_reading.properties");
        m_status_display.setText("Successfully saved settings for use.");
    }

    @FXML
    private void handleLaunchPositioning(ActionEvent event) {

    }
    @FXML
    private void handleLaunchMotionData(ActionEvent event) {

    }
    @FXML
    private void handleLaunchPositioningAndMotionData(ActionEvent event) {

    }

    private void update_variables_from_gui() {
        use_remote = String.valueOf(m_use_mobile_device.isSelected());
        remote_id = m_mobile_device_id.getText();
        anchor1_id = m_a1_id.getText();
        anchor1_x = m_a1_x.getText();
        anchor1_y = m_a1_y.getText();
        anchor1_z = m_a1_z.getText();
        anchor2_id = m_a2_id.getText();
        anchor2_x = m_a2_x.getText();
        anchor2_y = m_a2_y.getText();
        anchor2_z = m_a2_z.getText();
        anchor3_id = m_a3_id.getText();
        anchor3_x = m_a3_x.getText();
        anchor3_y = m_a3_y.getText();
        anchor3_z = m_a3_z.getText();
        anchor4_id = m_a4_id.getText();
        anchor4_x = m_a4_x.getText();
        anchor4_y = m_a4_y.getText();
        anchor4_z = m_a4_z.getText();

        log_pressure = String.valueOf(m_log_pressure.isSelected());
        log_acceleration = String.valueOf(m_log_acceleration.isSelected());
        log_magnetic = String.valueOf(m_log_magnetic.isSelected());
        log_angular_velocity = String.valueOf(m_log_angular_velocity.isSelected());
        log_euler_angles = String.valueOf(m_log_euler_angles.isSelected());
        log_quaternion = String.valueOf(m_log_quaternion.isSelected());
        log_linear_acceleration = String.valueOf(m_log_linear_acceleration.isSelected());
        log_gravity = String.valueOf(m_log_gravity.isSelected());

        use_file = String.valueOf(m_use_file.isSelected());
        filename = m_filename.getText();
        use_txt_ext = String.valueOf(m_use_txt_ext.isSelected());
        use_processing = String.valueOf(m_use_processing.isSelected());
    }

    private void save_properties_to_file(String file) {
        Properties props = new Properties();
        OutputStream output = null;
        if(!file.endsWith(".properties")) {
            file += ".properties";
        }
        try {

            output = new FileOutputStream(file);

            // set the properties value
            props.setProperty("use_remote", use_remote);
            props.setProperty("remote_id", remote_id);
            props.setProperty("anchor_1_id", anchor1_id);
            props.setProperty("anchor_1_x", anchor1_x);
            props.setProperty("anchor_1_y", anchor1_y);
            props.setProperty("anchor_1_z", anchor1_z);
            props.setProperty("anchor_2_id", anchor2_id);
            props.setProperty("anchor_2_x", anchor2_x);
            props.setProperty("anchor_2_y", anchor2_y);
            props.setProperty("anchor_2_z", anchor2_z);
            props.setProperty("anchor_3_id", anchor3_id);
            props.setProperty("anchor_3_x", anchor3_x);
            props.setProperty("anchor_3_y", anchor3_y);
            props.setProperty("anchor_3_z", anchor3_z);
            props.setProperty("anchor_4_id", anchor4_id);
            props.setProperty("anchor_4_x", anchor4_x);
            props.setProperty("anchor_4_y", anchor4_y);
            props.setProperty("anchor_4_z", anchor4_z);

            props.setProperty("log_pressure", log_pressure);
            props.setProperty("log_acceleration", log_acceleration);
            props.setProperty("log_magnetic", log_magnetic);
            props.setProperty("log_angular_velocity", log_angular_velocity);
            props.setProperty("log_euler_angles", log_euler_angles);
            props.setProperty("log_quaternion", log_quaternion);
            props.setProperty("log_linear_acceleration", log_linear_acceleration);
            props.setProperty("log_gravity", log_gravity);

            props.setProperty("use_file", use_file);
            props.setProperty("filename", filename);
            props.setProperty("use_txt_extension", use_txt_ext);
            props.setProperty("use_processing", use_processing);

            // save properties to project root folder
            props.store(output, null);

        } catch (IOException io) {
            io.printStackTrace();
        } finally {
            if (output != null) {
                try {
                    output.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

        }
    }

    private void load_properties_from_file(String loadPath) {
        if(!loadPath.endsWith(".properties")) {
            m_status_display.setText("Invalid file, cannot read properties");
            return;
        }
//        if(!loadPath.startsWith("/")) {
//            loadPath = "/" + loadPath;
//        }
        Properties prop = new Properties();
        try {
            //load a properties file from class path, inside static method
            FileInputStream stream = new FileInputStream(loadPath);
            prop.load(stream);
            //get the property value and print it out
            m_use_mobile_device.setSelected(Boolean.valueOf(prop.getProperty("use_mobile_device", "false")));
            m_mobile_device_id.setText(prop.getProperty("remote_id", ""));
            m_a1_id.setText(prop.getProperty("anchor_1_id", ""));
            m_a1_x.setText(prop.getProperty("anchor_1_x", ""));
            m_a1_y.setText(prop.getProperty("anchor_1_y", ""));
            m_a1_z.setText(prop.getProperty("anchor_1_z", ""));
            m_a2_id.setText(prop.getProperty("anchor_2_id", ""));
            m_a2_x.setText(prop.getProperty("anchor_2_x", ""));
            m_a2_y.setText(prop.getProperty("anchor_2_y", ""));
            m_a2_z.setText(prop.getProperty("anchor_2_z", ""));
            m_a3_id.setText(prop.getProperty("anchor_3_id", ""));
            m_a3_x.setText(prop.getProperty("anchor_3_x", ""));
            m_a3_y.setText(prop.getProperty("anchor_3_y", ""));
            m_a3_z.setText(prop.getProperty("anchor_3_z", ""));
            m_a4_id.setText(prop.getProperty("anchor_4_id", ""));
            m_a4_x.setText(prop.getProperty("anchor_4_x", ""));
            m_a4_y.setText(prop.getProperty("anchor_4_y", ""));
            m_a4_z.setText(prop.getProperty("anchor_4_z", ""));
            m_log_pressure.setSelected(Boolean.valueOf(prop.getProperty("log_pressure", "false")));
            m_log_acceleration.setSelected(Boolean.valueOf(prop.getProperty("log_acceleration", "false")));
            m_log_magnetic.setSelected(Boolean.valueOf(prop.getProperty("log_magnetic", "false")));
            m_log_angular_velocity.setSelected(Boolean.valueOf(prop.getProperty("log_angular_velocity", "false")));
            m_log_euler_angles.setSelected(Boolean.valueOf(prop.getProperty("log_euler_angles", "false")));
            m_log_quaternion.setSelected(Boolean.valueOf(prop.getProperty("log_quaternion", "false")));
            m_log_linear_acceleration.setSelected(Boolean.valueOf(prop.getProperty("log_linear_acceleration", "false")));
            m_log_gravity.setSelected(Boolean.valueOf(prop.getProperty("log_gravity", "false")));
            m_use_file.setSelected(Boolean.valueOf(prop.getProperty("use_file", "false")));
            m_filename.setText(prop.getProperty("filename", ""));
            m_use_txt_ext.setSelected(Boolean.valueOf(prop.getProperty("use_txt_extension", "false")));
            m_use_processing.setSelected(Boolean.valueOf(prop.getProperty("use_processing", "")));

            update_variables_from_gui();

            m_status_display.setText("Successfully loaded values.");
        }
        catch (IOException ex) {
            ex.printStackTrace();
        }
    }

//    @SuppressWarnings("SuspiciousNameCombination")
//    private void print_variables() {
//        System.out.println(use_remote);
//        System.out.println(remote_id);
//        System.out.println(anchor1_id);
//        System.out.println(anchor1_x);
//        System.out.println(anchor1_y);
//        System.out.println(anchor1_z);
//        System.out.println(anchor2_id);
//        System.out.println(anchor2_x);
//        System.out.println(anchor2_y);
//        System.out.println(anchor2_z);
//        System.out.println(anchor3_id);
//        System.out.println(anchor3_x);
//        System.out.println(anchor3_y);
//        System.out.println(anchor3_z);
//        System.out.println(anchor4_id);
//        System.out.println(anchor4_x);
//        System.out.println(anchor4_y);
//        System.out.println(anchor4_z);
//
//        System.out.println(log_pressure);
//        System.out.println(log_acceleration);
//        System.out.println(log_magnetic);
//        System.out.println(log_angular_velocity);
//        System.out.println(log_euler_angles);
//        System.out.println(log_quaternion);
//        System.out.println(log_linear_acceleration);
//        System.out.println(log_gravity);
//
//        System.out.println(use_file);
//        System.out.println(filename);
//        System.out.println(use_txt_ext);
//        System.out.println(use_processing);
//    }

    private static void configureFileChooser(final FileChooser fileChooser) {
        fileChooser.setTitle("Save Settings Template");
        fileChooser.setInitialDirectory(
                new File("./Configurations/")
        );
        fileChooser.getExtensionFilters().add(
                new FileChooser.ExtensionFilter("Properties", "*.properties")
        );
    }


}
