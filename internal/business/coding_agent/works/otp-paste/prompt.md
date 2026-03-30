The application is suffering from a state corruption bug on paste. The `OtpInput` component is not correctly handling paste events. Furthermore, `App.js` is passing the wrong prop (`inputCount` instead of `numInputs`), and the `CustomInput` component is not correctly forwarding its ref, which `OtpInput` requires.

Your task is to fix all these issues by implementing a custom `handlePaste` function, correcting the prop names, and properly implementing `React.forwardRef`.

**Strict Requirements:**

* **Dependency:** Your solution script **must install** `react-otp-input` version `3.1.1` by editing `package.json` and running `npm install`.

* **File 1 (`src/App.js`):** You must refactor this file to:
    1.  Import `Verification` from `./Verification`.
    2.  Pass the correct prop `numInputs={6}` to the `<Verification />` component.
    3.  **Do not** pass the old `inputCount` prop.

* **File 2 (`src/CustomInput.js`):** You must refactor this file to:
    1.  Use `React.forwardRef` to correctly wrap the component.
    2.  Pass the forwarded `ref` to the `<input>` element.

* **File 3 (`src/Verification.js`):** This is the core of the fix. You must refactor this component to:
    1.  Accept the `numInputs` prop.
    2.  Import `CustomInput` from `./CustomInput`.
    3.  Import `StateDisplay` from `./StateDisplay`.
    4.  Implement a `handlePaste` function. This function must:
        * Access the clipboard data (e.g., `e.clipboardData.getData('text')`).
        * Call `setOtp` with the pasted data, slicing it to the `numInputs` prop.
    5.  Pass the `handlePaste` function to the `<OtpInput />` component's `onPaste` prop.
    6.  The `renderInput` prop must be updated to use the `CustomInput` component.
    7.  Render the `<StateDisplay />` component, passing the `otp` state to it.

* **File 4 (`src/StateDisplay.js`):** You must refactor this file to:
    1.  Change the text inside the `<pre>` tag to be `Code: {otp || 'empty'}`.

* **Server Management:** Your solution script must start the React development server, verify it's running at `http://localhost:3000` and log its output to '/app/server.log'. The server log must compile successfully without errors.
* **Build:** The build (`npm run build`) must complete successfully, which should be verified and log its output to '/tmp/build.log'.
* **Proof of Work:** The solution script must create a receipt file at `/app/solution_receipt.txt` and log "Solution script completed successfully" to it.
