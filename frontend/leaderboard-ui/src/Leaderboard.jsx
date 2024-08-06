import { useState } from "react"

export const Leaderboard = () => {
    const [scores, setScores] = useState(null);
    const [showScores, setShowScores] = useState(false);

    const fetchScores = () => {
        const url = '/score';
        fetch(url)
            .then(resp => resp.json())
            .then(data => {
                console.log(`GOt the data back ${JSON.stringify(data)}`);
                const sArr = new Array();
                data.scores.forEach(s => {
                    sArr.push(s);
                })
                setScores(sArr);
                console.log(sArr);
                setShowScores(!showScores);
            })
    }
    const arrayDataItems = scores && scores.map(s =>
        <tr key={s.username}>
            <td>{s.username}</td>
            <td>{s.score}</td>
        </tr>
    )

    return (
        <div>
            <h2> Your top scores</h2>
            <div>
                <p>
                    {showScores ? <button onClick={fetchScores}> Hide Scores</button> : <button onClick={fetchScores}> Show Scores</button>}

                </p>
                <h3> About to show scores </h3>
                {showScores ?
                    <table style={{
                        border: "2px solid grey",
                        marginLeft: "auto",
                        marginRight: "auto",
                        padding: 8,
                    }}>
                        <tbody>
                            <tr>
                                <th> Username </th>
                                <th> Score </th>
                            </tr>

                            {arrayDataItems}
                        </tbody>
                    </table>
                    : <></>
                }
            </div>
        </div>
    )
}