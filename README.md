## QWebview-plus
 - 키움 오픈 API for JavaScript를 지원
 
## 키움 open api를 제공
 
### window.kiwoom 
 - [키움 오픈 API](https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.1.pdf)와 동일한 메소드를 제공
 - 키움 오픈 API와 네이밍 규칙이 다름 
    - 첫 문자가 대문자 아닌 소문자
      ```
      예) CommConnect => commConnect
      ```

### 이벤트
 - [키움 오픈 API](https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.1.pdf)와 동일한 이벤트를 제공
 - 모든 이벤트는 document에서 발생한다.
 - 키움 오픈 API와 네이밍 규칙이 다름 
    - `kiwoom` 이라는 event namespace가 붙음
    - 이벤트 명에서 `on`이라는 prefix가 제거하고, 첫 문자를 소문자로 변경
      ```
      예) OnReceiveTrData => receiveTrData.kiwoom
      ```
    - 이벤트에 의해 전달되는 속성은 detail에 포함되어 전달됨
    - 이벤트에 전달되는 속성명은 타입약어가 제거되고, 첫 문자를 소문자로 변경
      ```
      예) sScrNo => scrNo
      ```
