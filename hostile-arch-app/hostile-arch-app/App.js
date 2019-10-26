import React, { Component } from "react";
import { StyleSheet, Text, View, Button, Alert, TextInput } from "react-native";
import Picture from "./components/Picture";
import Email from "./components/Email";
import Location from "./components/Location";
import Camera from "./components/Camera"

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      location: false,
      description: null,
    };
  }

  handleClick = event => {
    this.setState({
      location: true
    });
  };

  onChangeText = (text) => {
    this.setState({
      description: text
    })
  }

  render() {
    return (
      <View style={styles.container}>
        {/* <Text style={styles.welcome}>Hello</Text> */}
        <Camera />
        <TextInput placeholder="Enter image description here!"
          style={styles.description}
          onChangeText={text => this.onChangeText(text)}
        />
        {/* <Button
          title="Get Location"
          onPress={e => this.handleClick(e)}
        ></Button> */}
        {this.state.location === true && <Location />}

        <TextInput placeholder="Enter email address! (Optional)"
          style={styles.email}
          onChangeText={text => this.onChangeText(text)}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5FCFF"
  },
  welcome: {
    fontSize: 20,
    textAlign: "center",
    margin: 10
  },
  instructions: {
    textAlign: "center",
    marginBottom: 5
  },
  description: {
    height: 40, 
    width: 480,
    borderColor: 'gray', 
    borderWidth: 1,
    borderBottomWidth: 0.45,
    textAlign: "center",
    marginLeft: 10

  },
  email: {
    height: 40, 
    width: 480,
    borderColor: 'gray', 
    borderWidth: 1,
    borderTopWidth: 0.45,
    textAlign: "center",
    marginLeft: 10,
  }
});
