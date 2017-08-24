package psupozyx;

import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.stage.Stage;
import sun.rmi.log.LogOutputStream;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ResourceBundle;

public class ConsoleWindow implements Initializable {
    @FXML
    private Label console;

    private Process pr;

    void launchPyScript(String py_script_name) {
        console.setText("");
        new Thread(() -> {
            try {
                ProcessBuilder ps=new ProcessBuilder("python", py_script_name);

                ps.redirectErrorStream(true);

                pr = ps.start();

                BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()), 16);
                String line;


                int timePos;
                float pyElapsedTime;

                double delayTime = 3.0;

                long newTime;
                long nanodifference;
                long oldTime = System.nanoTime();
                float secondDif;


                // read python script output
                while ((line = in.readLine()) != null) {


                    // if the line has time information
                    if (line.contains(" Time: ")) {
                        // is a data line
                        timePos = line.indexOf("Time:");
                        pyElapsedTime = 1 * Float.parseFloat((line.substring(timePos + 6, timePos + 16)));


                        newTime = System.nanoTime();
                        nanodifference = newTime - oldTime;
                        secondDif = (float) (nanodifference / 1000000000.0);
                        // Thread.sleep(5);
                        while (secondDif < (pyElapsedTime + delayTime)) {
                            newTime = System.nanoTime();
                            nanodifference = newTime - oldTime;
                            secondDif = (float) (nanodifference / 1000000000.0);
                            Thread.sleep(5);
                        }

                    } else {
                        Thread.sleep(30);
                    }



                    // add input line to the top of the textarea
                    // if I comment this out, no errors

                    final String finalLine = line;
                    javafx.application.Platform.runLater( () -> console.setText(finalLine + '\n' + console.getText()));



                    // for debugging
                    System.out.println(String.valueOf(line));
                }
                pr.waitFor();
                System.out.println("ok!");

                in.close();

            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }).start();


    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        console.setText("Waiting for script to collect data...\n");
    }


    void terminateProcess() {
        if (pr != null) {
            pr.destroy();
        }
    }

}
