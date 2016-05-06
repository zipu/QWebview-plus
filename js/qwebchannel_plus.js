"use strict";
// QWebchannel 사용 예
new QWebChannel(qt.webChannelTransport, function(channel){
    let kiwoom = window.kiwoom = channel.objects.kiwoom;
    // __로 시작 안하는
    const keywords = [ "unwrapQObject", "unwrapProperties", "propertyUpdate", "signalEmitted", "deleteLater", "objectNameChanged",
    "destroyed", "bridge" ];

    // 메소드 호출
    for(let p in kiwoom) {
        // kw_로 시작 하는 메소드
        if(!p.startsWith("__") && keywords.indexOf(p) === -1) {
            let orgFn = window.kiwoom[p];
            window.kiwoom[p] = function() {
                let methodArgs = Array.prototype.slice.call(arguments);
                return new Promise( resolve => {
                    methodArgs.push(ret => resolve(ret));
                    orgFn.apply(kiwoom, methodArgs);
                });
            };
        }
    }
    // 이벤트 처리
    kiwoom.bridge.connect(function(eventName, data){
        let event = document.createEvent("CustomEvent");
        event.initCustomEvent(eventName, true, true, JSON.parse(data));
        document.dispatchEvent(event);
    });
});
