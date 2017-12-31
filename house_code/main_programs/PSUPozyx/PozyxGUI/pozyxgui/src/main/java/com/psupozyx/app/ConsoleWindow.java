package com.psupozyx.app;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ResourceBundle;

public class ConsoleWindow implements Initializable {
    @FXML
    private Label console;

    private Process pr;

    private static final int CHARACTERDISPLAYBUFFER = 30000;

    private String osName = System.getProperty("os.name");
    private String OS = osName.toLowerCase();

    void launchScript(String startMessage, String executable, String prependPathType) {
        if (startMessage != null) {
            console.setText(startMessage);
        }

        console.setText("Running " + executable + " on " + osName + '\n');
        new Thread(() -> {
            try {
                Controller controller = new Controller();
                String executableWithDirectory = controller.traverseUpToRootFolder();;
                if (isWindows()) {
                    executableWithDirectory += "scripts/win/" + executable + "/" + executable + ".exe";
                }
                else if (isMac()) {
                    executableWithDirectory += "build/exe.macosx-10.6-intel-3.6/" + executable + ".app";
                }
                else if (isUnix()) {
                    executableWithDirectory += "scripts/unix/" + executable + "/" + executable + ".deb";
                }
                else {
                    console.setText("Unfortunately your operating system is not yet supported.\n" +
                            "Please try again on a Windows, Mac, or Linux device.");
                    throw new NotImplementedException();
                }


                ProcessBuilder ps=new ProcessBuilder(executableWithDirectory);

                ps.redirectErrorStream(true);

                pr = ps.start();
                InputStream inputStream = pr.getInputStream();

                BufferedReader in = new BufferedReader(new InputStreamReader(inputStream), 2048);
                String line;
                String pooledOutput;

                // read python script output
                while ((line = in.readLine()) != null) {

                    pooledOutput = line + '\n' + console.getText();
                    if(pooledOutput.length() >= CHARACTERDISPLAYBUFFER) {
                        pooledOutput = pooledOutput.substring(0, CHARACTERDISPLAYBUFFER);
                    }
                    final String finalOutput = pooledOutput;
                    Platform.runLater( () -> console.setText(finalOutput));
                }
                pr.waitFor();

                in.close();

            } catch (IOException | InterruptedException e) {
                console.setText(e.toString() + console.getText());
                e.printStackTrace();
            }
        }).start();
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
    }

    void terminateProcess() {
        if (pr != null) {
            pr.destroy();
        }
    }


    private boolean isWindows() {
        return (OS.contains("win"));
    }

    private boolean isMac() {
        return (OS.contains("mac"));
    }

    private boolean isUnix() {
        return (OS.contains("nix") || OS.contains("nux") || OS.indexOf("aix") > 0 );
    }

    private boolean isSolaris() {
        return (OS.contains("sunos"));
    }
}
