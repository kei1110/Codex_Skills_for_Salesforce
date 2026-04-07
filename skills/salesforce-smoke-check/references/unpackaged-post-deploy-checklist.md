# Unpackaged Post Deploy Checklist

- package install 後に必要な activation / assignment が終わっているか
- smoke 対象 org に必要な unpackaged metadata がその環境の deploy path で実際に入っているか
- source deploy 不可の metadata は手動設定済みか
- FlexiPage、Layout、Record Type、Permission Set の反映順が崩れていないか
- post deploy 後に確認すべき代表導線が smoke に含まれているか
