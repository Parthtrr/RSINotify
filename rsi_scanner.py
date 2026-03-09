import yfinance as yf
import pandas as pd

etfs = {
"NIFTYBEES.NS":39,
"JUNIORBEES.NS":35,
"HDFCMID150.NS":39,
"HDFCSML250.NS":37,
"BANKBEES.NS":40.5,
"PVTBANIETF.NS":39.28,
"PSUBNKBEES.NS":37,
"FINIETF.NS":41,
"AUTOBEES.NS":37,
"FMCGIETF.NS":37,
"ITBEES.NS":30,
"PHARMABEES.NS":35.6,
"HEALTHY.NS":36.5,
"METALIETF.NS":30,
"OILIETF.NS":35,
"INFRABEES.NS":32.5,
"ABSLPSE.NS":31.17,
"CPSEETF.NS":31,
"MODEFENCE.NS":31.5,
"TNIDETF.NS":30,
"MON100.NS":40.5,
"MASPTOP50.NS":35.8,
"HNGSNGBEES.NS":32,
"MAHKTECH.NS":32.85,
"GOLDBEES.NS":32.62,
"SILVERBEES.NS":32.33,
"COMMOIETF.NS":33.55,
"MAFANG.NS":33.95
}


def rsi_tv(close, length=14):

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/length, adjust=False).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100/(1+rs))

    return rsi


def scan_rsi():

    messages = []

    for ticker, benchmark in etfs.items():

        df = yf.download(
            ticker,
            period="10y",
            interval="1d",
            progress=False
        )

        if df.empty:
            continue

        # Fix yfinance multi-index columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Convert daily data to weekly (includes running week)
        weekly = df.resample("W-FRI").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

        weekly["RSI"] = rsi_tv(weekly["Close"])

        current_rsi = weekly["RSI"].iloc[-1]

        print(f"Ticker = {ticker} | Current Weekly RSI = {round(current_rsi,2)}")

        diff = benchmark - current_rsi

        signal = "NO BUY"

        if 0 <= diff < 4:
            signal = "BUY 1X"

        elif 4 <= diff < 8:
            signal = "BUY 2X"

        elif diff >= 8:
            signal = "BUY 3X"

        if signal != "NO BUY":

            msg = (
                f"{ticker}\n"
                f"CurrentRSI : {round(current_rsi,2)}\n"
                f"BenchmarkRSI : {benchmark}\n"
                f"Signal : {signal}\n"
            )

            messages.append(msg)

    return messages


if __name__ == "__main__":

    signals = scan_rsi()

    print("\nBUY SIGNALS\n")

    for s in signals:
        print(s)