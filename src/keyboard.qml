import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.VirtualKeyboard 2.15
import QtQuick.VirtualKeyboard.Styles 2.15



Item {
    id: windowK
    x: 0
    y: 320
    
    
	
    Rectangle
    {
        id: backgroundK
	anchors.centerIn: parent
    	width: 1000
    	height: 1000
        color: "black"
    }

    InputPanel {
        id: inputPanelK
        width: windowK.width
        height: windowK.height
	property var isKeyboardActive: inputPanel.active 
        objectName: "inputPanel_object"

        states: State {
            name: "visible"
            when: inputPanelK.active
            PropertyChanges {
                target: windowK
                height: inputPanelK.height
                y: windowK.height - inputPanelK.height
            }
        }
        transitions: Transition {
            from: ""
            to: "visible"
            reversible: true
            ParallelAnimation {
                NumberAnimation {
                    properties: "y"
                    duration: 250
                    easing.type: Easing.InOutQuad
                }
            }
        }
    }
}

