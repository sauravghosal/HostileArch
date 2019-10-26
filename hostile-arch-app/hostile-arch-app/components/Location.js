import React, {Component} from 'react'
import {View,Text} from 'react-native'

type Props = {};
export default class Location extends Component<Props> {
    constructor(props) {
        super(props)

        this.state = {
            initialPosition: {
                latitude: 0,
                longitude: 0,
            },
            markerPosition: {
                latitude: 0,
                longitude: 0
            }
        }
    }

    componentDidMount() {
        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                this.setState({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            },
            (error) => {
                this.setState({ error: error.message})
            },
            { enableHighAccuracy: false, timeout: 1, maximumAge: 1, distanceFilter: 1}
        )
    }

    render() {
        return (
            <View>
                { (this.state.latitude && this.state.longitude) 
                ? 
                <Text> My location is: { this.state.latitude }, { this.state.longitude }</Text>
                :
                <Text>Location services not enabled</Text>
            }
            </View>
        )
    }



}
