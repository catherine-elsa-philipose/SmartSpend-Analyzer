import { useState } from "react";

export default function Signup() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSignup = async() => {
        try {
            const res = await fetch("http://127.0.0.1:5000/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            const data = await res.json();
            console.log(data);

            if (res.status === 201) {
                alert("Signup successful ✅");
            } else {
                alert(data.message || "Signup failed");
            }
        } catch (err) {
            console.error(err);
            alert("Error connecting to backend");
        }
    };

    return ( <
        div style = {
            { padding: "40px" }
        } >
        <
        h2 > Signup < /h2>

        <
        input placeholder = "Username"
        value = { username }
        onChange = {
            (e) => setUsername(e.target.value)
        }
        /> <
        br / > < br / >

        <
        input type = "password"
        placeholder = "Password"
        value = { password }
        onChange = {
            (e) => setPassword(e.target.value)
        }
        /> <
        br / > < br / >

        <
        button onClick = { handleSignup } > Sign Up < /button> < /
        div >
    );
}