import React, { Component } from "react";
import { View, Text, StyleSheet, ActivityIndicator } from "react-native";

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
    this.setState({
      ready: true,
      where: { lat: position.coords.latitude, lng: position.coords.longitude }
    });

    this.props.changeLat(this.state.where.lat);
    this.props.changeLong(this.state.where.lng);
  };
  geoFailure = err => {
    this.setState({ error: err.message });
  };
  render() {
    return (
      <>
        {!this.state.ready && (
          <ActivityIndicator size="large" color="#0000ff" />
        )}
        {this.state.error && (
          <Text style={styles.welcome}>{this.state.error}</Text>
        )}
        {this.state.ready && (
          <Text style={styles.welcome}>{`Latitude: ${this.state.where.lat}
            Longitude: ${this.state.where.lng}`}</Text>
        )}
      </>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5FCFF",
    alignItems: "center",
    justifyContent: "center"
  },
  welcome: {
    fontSize: 20,
    textAlign: "center",
    margin: 10
  }
});
