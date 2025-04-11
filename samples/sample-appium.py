# Simple example of usage of caqui with Android App
# It opens the app and get the source code
# Appium configured using docker for simplicity
# https://hub.docker.com/r/appium/appium/
# sample app in ./tests/apk folder
from caqui import synchronous


def main():
    driver_url = "http://127.0.0.1:4723"
    capabilities = {
        "capabilities": {
            "firstMatch": [{}],
            "alwaysMatch": {
                "appium:automationName": "UIAutomator2",
                "platformName": "Android",
                "appium:udid": "YOUR-APP-UUID",  # replace with your device uuid
                "appium:app": "/home/androidusr/sample.apk",  # refereces the folder in docker container
            },
        }
    }

    session = synchronous.get_session(driver_url, capabilities)
    print("session: ", session)

    source = synchronous.get_page_source(driver_url, session)
    print("source: ", source)

    synchronous.close_session(driver_url, session)


if __name__ == "__main__":
    main()

# output
# python sample-appium.py
# session:  8264988f-2c63-4935-a46f-3aa8ccc09004
# source:  <?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
# <hierarchy index="0" class="hierarchy" rotation="0" width="720" height="1472">
#   <android.widget.FrameLayout index="0" package="com.example.sample" class="android.widget.FrameLayout" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][720,1472]" displayed="true">
#     <android.widget.LinearLayout index="0" package="com.example.sample" class="android.widget.LinearLayout" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][720,1472]" displayed="true">
#       <android.widget.FrameLayout index="0" package="com.example.sample" class="android.widget.FrameLayout" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][720,1472]" displayed="true">
#         <android.widget.LinearLayout index="0" package="com.example.sample" class="android.widget.LinearLayout" text="" resource-id="com.example.sample:id/action_bar_root" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][720,1472]" displayed="true">
#           <android.widget.FrameLayout index="0" package="com.example.sample" class="android.widget.FrameLayout" text="" resource-id="android:id/content" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][720,1472]" displayed="true">
#             <android.view.ViewGroup index="0" package="com.example.sample" class="android.view.ViewGroup" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][720,1472]" displayed="true">
#               <android.widget.LinearLayout index="0" package="com.example.sample" class="android.widget.LinearLayout" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,0][720,159]" displayed="true">
#                 <android.view.ViewGroup index="0" package="com.example.sample" class="android.view.ViewGroup" text="" resource-id="com.example.sample:id/toolbar" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,47][720,159]" displayed="true">
#                   <android.widget.TextView index="0" package="com.example.sample" class="android.widget.TextView" text="First Fragment" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[28,76][282,129]" displayed="true" />
#                   <androidx.appcompat.widget.LinearLayoutCompat index="1" package="com.example.sample" class="androidx.appcompat.widget.LinearLayoutCompat" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[649,54][720,152]" displayed="true">
#                     <android.widget.ImageView index="0" package="com.example.sample" class="android.widget.ImageView" text="" content-desc="More options" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="true" password="false" scrollable="false" selected="false" bounds="[649,61][720,145]" displayed="true" />
#                   </androidx.appcompat.widget.LinearLayoutCompat>
#                 </android.view.ViewGroup>
#               </android.widget.LinearLayout>
#               <android.view.ViewGroup index="1" package="com.example.sample" class="android.view.ViewGroup" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,159][720,1472]" displayed="true">
#                 <android.widget.FrameLayout index="0" package="com.example.sample" class="android.widget.FrameLayout" text="" resource-id="com.example.sample:id/nav_host_fragment_content_main" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,159][720,1472]" displayed="true">
#                   <android.widget.ScrollView index="0" package="com.example.sample" class="android.widget.ScrollView" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="true" selected="false" bounds="[0,159][720,1472]" displayed="true">
#                     <android.view.ViewGroup index="0" package="com.example.sample" class="android.view.ViewGroup" text="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[0,159][720,1472]" displayed="true">
#                       <android.widget.Button index="0" package="com.example.sample" class="android.widget.Button" text="Next" resource-id="com.example.sample:id/button_first" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[283,187][437,271]" displayed="true" />
#                       <android.widget.TextView index="1" package="com.example.sample" class="android.widget.TextView" text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam in scelerisque sem. Mauris volutpat, dolor id interdum ullamcorper, risus dolor egestas lectus, sit amet mattis purus dui nec risus. Maecenas non sodales nisi, vel dictum dolor. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse blandit eleifend diam, vel rutrum tellus vulputate quis. Aliquam eget libero aliquet, imperdiet nisl a, ornare ex. Sed rhoncus est ut libero porta lobortis. Fusce in dictum tellus.&#10;&#10; Suspendisse interdum ornare ante. Aliquam nec cursus lorem. Morbi id magna felis. Vivamus egestas, est a condimentum egestas, turpis nisl iaculis ipsum, in dictum tellus dolor sed neque. Morbi tellus erat, dapibus ut sem a, iaculis tincidunt dui. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur et eros porttitor, ultricies urna vitae, molestie nibh. Phasellus at commodo eros, non aliquet metus. Sed maximus nisl nec dolor bibendum, vel congue leo egestas.&#10;&#10; Sed interdum tortor nibh, in sagittis risus mollis quis. Curabitur mi odio, condimentum sit amet auctor at, mollis non turpis. Nullam pretium libero vestibulum, finibus orci vel, molestie quam. Fusce blandit tincidunt nulla, quis sollicitudin libero facilisis et. Integer interdum nunc ligula, et fermentum metus hendrerit id. Vestibulum lectus felis, dictum at lacinia sit amet, tristique id quam. Cras eu consequat dui. Suspendisse sodales nunc ligula, in lobortis sem porta sed. Integer id ultrices magna, in luctus elit. Sed a pellentesque est.&#10;&#10; Aenean nunc velit, lacinia sed dolor sed, ultrices viverra nulla. Etiam a venenatis nibh. Morbi laoreet, tortor sed facilisis varius, nibh orci rhoncus nulla, id elementum leo dui non lorem. Nam mollis ipsum quis auctor varius. Quisque elementum eu libero sed commodo. In eros nisl, imperdiet vel imperdiet et, scelerisque a mauris. Pellentesque varius ex nunc, quis imperdiet eros placerat ac. Duis finibus orci et est auctor tincidunt. Sed non viverra ipsum. Nunc quis augue egestas, cursus lorem at, molestie sem. Morbi a consectetur ipsum, a placerat diam. Etiam vulputate dignissim convallis. Integer faucibus mauris sit amet finibus convallis.&#10;&#10; Phasellus in aliquet mi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In volutpat arcu ut felis sagittis, in finibus massa gravida. Pellentesque id tellus orci. Integer dictum, lorem sed efficitur ullamcorper, libero justo consectetur ipsum, in mollis nisl ex sed nisl. Donec maximus ullamcorper sodales. Praesent bibendum rhoncus tellus nec feugiat. In a ornare nulla. Donec rhoncus libero vel nunc consequat, quis tincidunt nisl eleifend. Cras bibendum enim a justo luctus vestibulum. Fusce dictum libero quis erat maximus, vitae volutpat diam dignissim." resource-id="com.example.sample:id/textview_first" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[28,299][692,1472]" displayed="true" />
#                     </android.view.ViewGroup>
#                   </android.widget.ScrollView>
#                 </android.widget.FrameLayout>
#               </android.view.ViewGroup>
#               <android.widget.ImageButton index="2" package="com.example.sample" class="android.widget.ImageButton" text="" resource-id="com.example.sample:id/fab" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" long-clickable="false" password="false" scrollable="false" selected="false" bounds="[594,1390][692,1472]" displayed="true" />
#             </android.view.ViewGroup>
#           </android.widget.FrameLayout>
#         </android.widget.LinearLayout>
#       </android.widget.FrameLayout>
#     </android.widget.LinearLayout>
#   </android.widget.FrameLayout>
# </hierarchy>
