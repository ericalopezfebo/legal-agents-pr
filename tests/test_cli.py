from legal_agents_pr.cli.main import main


def test_cli_list(capsys):
    assert main(["list"]) == 0
    assert "administrative-law" in capsys.readouterr().out


def test_cli_route(capsys):
    assert main(["route", "revisión judicial de agencia"]) == 0
    assert "administrative-law" in capsys.readouterr().out
