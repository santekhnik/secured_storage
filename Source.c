#include <stdint.h>
#include <stdio.h>

// Function to calculate BCC
uint8_t CalculateBCC(const uint8_t* data, uint16_t length) {
    uint8_t bcc = 0x00; //The initial value of BCC
    printf("Initial BCC: 0x%02X\n", bcc);

    for (uint16_t i = 0; i < length; i++) {
        printf("Data[%d]: 0x%02X, BCC before XOR: 0x%02X\n", i, data[i], bcc);
        bcc ^= data[i]; // XOR each byte with the current BCC value
        printf("BCC after XOR: 0x%02X\n", bcc);
    }

    return bcc;
}

int main() {
    //Enter arbitrary data
    uint8_t data[] = { 0x11, 0x36, 0x56, 0x78, 0x9A }; // Replace the values ​​with any
    uint16_t length = sizeof(data) / sizeof(data[0]);

    // Output of the initial data array
    printf("Data array: ");
    for (uint16_t i = 0; i < length; i++) {
        printf("0x%02X ", data[i]);
    }
    printf("\n");

    // Calculation of BCC
    uint8_t bcc = CalculateBCC(data, length);

    // Conclusion of the final result
    printf("Final BCC: 0x%02X\n", bcc);

    return 0;
}
