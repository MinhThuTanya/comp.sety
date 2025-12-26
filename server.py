#include <iostream>
#include <string> 
#include "winsock2.h"

#pragma comment (lib, "Ws2_32.lib")
#pragma warning(disable: 4996)
#define MAX_PACKET_SIZE 4096

using namespace std;

int main() {
    WSADATA ws;
    SOCKET s;
    sockaddr_in adr;
    hostent* hn;
    char buff[MAX_PACKET_SIZE];


    if (WSAStartup(MAKEWORD(2, 2), &ws) != 0) { 
        cerr << "WSAStartup failed." << endl;
        return -1;
    }

    if (INVALID_SOCKET == (s = socket(AF_INET, SOCK_STREAM, 0))) {
        cerr << "socket failed: " << WSAGetLastError() << endl;
        WSACleanup();
        return -1;
    }

    if (NULL == (hn = gethostbyname("www.json.org"))) {
        cerr << "gethostbyname failed." << endl;
        closesocket(s);
        WSACleanup();
        return -1;
    }

    adr.sin_family = AF_INET;
    adr.sin_addr.s_addr = *((unsigned long*)hn->h_addr_list[0]);
    adr.sin_port = htons(80);

    if (SOCKET_ERROR == connect(s, (sockaddr*)&adr, sizeof(adr))) {
        cerr << "connect failed: " << WSAGetLastError() << endl;
        closesocket(s);
        WSACleanup();
        return -1;
    }

    const char* request = "GET /json-ru.html HTTP/1.1\r\nHost: www.json.org\r\nConnection: keep-alive\r\n\r\n";
      //#define request "GET /json-ru.html HTTP/1.0 \r\n Host:www.json.org\r\n\r\n"

    if (SOCKET_ERROR == send(s, request, strlen(request), 0)) {
        cerr << "send failed: " << WSAGetLastError() << endl;
        closesocket(s);
        WSACleanup();
        return -1;
    }

    int len;
    do {
        len = recv(s, buff, MAX_PACKET_SIZE - 1, 0); 
        if (len == SOCKET_ERROR) {
            cerr << "recv failed: " << WSAGetLastError() << endl;
            closesocket(s);
            WSACleanup();
            return -1;
        }
        if (len > 0) {
            buff[len] = '\0';
            cout << buff;
        }
    } while (len > 0);


    if (SOCKET_ERROR == closesocket(s)) {
        cerr << "closesocket failed: " << WSAGetLastError() << endl;
    }

    WSACleanup();
    return 0;
}
