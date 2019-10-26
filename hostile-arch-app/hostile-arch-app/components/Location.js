import React, { Component } from "react";
import { View, Text, StyleSheet } from "react-native";

export default class Location extends Component {
  constructor() {
    super();
    this.state = {
      ready: false,
      where: { lat: null, lng: null },
      error: null
    };
  }
  componentDidMount() {
    let geoOptions = {
      enableHighAccuracy: true,
      timeOut: 20000,
      maximumAge: 60 * 60 * 24
    };
    this.setState({ ready: false, error: null });
    navigator.geolocation.getCurrentPosition(
      this.geoSuccess,
      this.geoFailure,
      geoOptions
    );
  }

  geoSuccess = position => {
    console.log(position.coords);

    this.setState({
      ready: true,
      where: { lat: position.coords.latitude, lng: position.coords.longitude }
    });

    console.log(this.state.where);
    console.log(this.state.ready);
  };
  geoFailure = err => {
    this.setState({ error: err.message });
  };
  render() {
    return (
      <View style={styles.container}>
        {!this.state.ready && (
          <Text style={styles.big}>Using Geolocation in React Native.</Text>
        )}
        {this.state.error && <Text style={styles.big}>{this.state.error}</Text>}
        {this.state.ready && (
          <Text style={styles.big}>{`Latitude: ${this.state.where.lat}
            Longitude: ${this.state.where.lng}`}</Text>
        )}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000000",
    alignItems: "center",
    justifyContent: "center"
  },
  big: {
    fontSize: 48,
    color: "#000000"
  }
});
