#encoding=utf-8

s = """

Grammar checking is a major part of Natural Language Processing (NLP) whose applications ranges from proofreading
to language learning. Much work has been done for the development of grammar checking tools in the past decade.
However, fewer efforts are made for surveying the existing literature. Thus, we present a comprehensive study of English
grammar checking techniques highlighting the capabilities and challenges associated with them. Also, we systematically
selected, examined and reviewed 12 approaches of Grammar checking. The 12 approaches can be classified into three
categories namely (1) Rule based technique, (2) Machine learning based technique, and (3) Hybrid technique. Each
technique has its own advantages and limitations. Rule based techniques are best suited for language learning but rule
designing is a laborious task. Machine learning alleviates this labor but it is dependent on the size and type of the
corpus used. Hybrid technique combines the best of both techniques but each part of the hybrid technique should be
implemented according to its suitability.
In this paper, we have also presented an error classification scheme which identifies five types of errors namely
sentence structure errors, punctuation errors, spelling errors, syntax errors, and semantic errors. These errors are
further subcategorized. This classification scheme would help the researchers and developers in following ways: (1)
identifying the most frequent errors would tell what type of errors must be targeted for correction, (2) identifying the
level of the error would tell what length of text should be examined to detect any error, (3) identifying the cause of
invalid text would help in finding a solution to write a valid text. This simplifies the task of grammar checking.
Based on our detailed review of various approaches, our observations are as follows: (1) No existing approach is
completely able to detect all types of errors efficiently, (2) Most of the tools are not available for research or public use,
(3) All approaches use different experimental data, thus it is hard to compare the results. (4) Most of the approaches have
addressed syntax errors and its subtypes while very few efforts have been done to detect errors at sentence level and at
semantic level. (5) Detection and correction of run-on sentences is yet another untouched research area, (6) No tools are
suitable for real time applications like proofreading of technical papers, language tutoring, writing assistance etc. (7) Our
research question RQ9 is still unanswered since we could not check the results of individual error types against gold standards, (8) Although, performance of tools has been improved gradually with time; there is much scope for improvements.

"""

s = s.replace("\n", " ")
print s