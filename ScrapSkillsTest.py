'''
python -m pytest ScrapSkillsTest.py
# python -m pytest ScrapSkillsTest.py -vvv


'''

from ScrapSkills import *
import pytest

print(generate_URL("python"))
print()
print(generate_URL("python ROWER "))
print()
print(generate_URL("python  junior"))
print()
print(generate_URL("python  junior trainee"))
print()
print(generate_URL("python php react"))


class TestScrapSkills:

    def test_generate_URL_a(self):
        # given
        keywords_1 = "python" # junior" # trainee"
        # when
        result_1 = generate_URL(keywords_1)
        # then
        assert result_1 == "https://nofluffjobs.com/pl/praca-it/python"

    def test_generate_URL_b(self):
        keywords_2 = "python zdalnie" 
        result_2 = generate_URL(keywords_2)
        assert result_2 == "https://nofluffjobs.com/pl/praca-it/praca-zdalna/python"

    def test_generate_URL_c(self):
        keywords_3 = "python Junior" # trainee"
        result_3 = generate_URL(keywords_3)
        assert result_3 == "https://nofluffjobs.com/pl/praca-it/python?criteria=seniority%3Djunior"
    
    def test_generate_URL_d(self):
        keywords_4 = "python Junior trainee"
        result_4 = generate_URL(keywords_4)
        assert result_4 == "https://nofluffjobs.com/pl/praca-it/python?criteria=seniority%3Dtrainee,junior"

    def test_generate_URL_e(self):
        keywords_5 = "python Junior rower aws warszawa Białystok trainee"
        result_5 = generate_URL(keywords_5)
        assert result_5 == "https://nofluffjobs.com/pl/praca-it/warszawa/python?criteria=city%3Dbialystok%20seniority%3Dtrainee,junior%20requirement%3Daws"

    # def test_generate_URL_wrong_keyword(self):
    #     keywords_6 = "rower"
    #     with pytest.raises(WrongKeyword):
    #         generate_URL(keywords_6)



    def test_exclude_unnecessary(self):
        # given
        words = 'all you base are belong to us'.split()
        to_exclude = 'all base are'.split()
        # when
        result = exclude_unnecessary(words, to_exclude)
        # then
        assert result == "you belong to us".split()

    def test_print_most_common(self, capsys):
        # given
        words = ["a"] * 5 + ["b"] * 15 + ["c"] * 7 + list("qwertyuiop") + list("iop")
        # number = 3
        
        # when
        print_most_common(words, 3)
        out_1, err_1 = capsys.readouterr()

        print_most_common(words[:20], 3)
        out_2, err_2 = capsys.readouterr()
        
        # then
        assert out_1 == "b -> 15\nc -> 7\na -> 5\n"
        assert out_2 == "b -> 15\na -> 5\n"

