class SummaryTools(object):
	
	def __init__(self,tittle,content):
		self.tittle = tittle
		self.content = content

	def split_content_to_sentences(self):
		content = self.content.replace('\n','. ')
		return content.split('. ')

	def split_content_to_paragraphs(self):
		return self.content.split('\n\n')

	def sentences_intersection(self, sent1, sent2):
		s1 = set(sent1.split(" "))
		s2 = set(sent2.split(" "))
		if len(s1) + len(s2) == 0: return 0
		return len(s1.intersection(s2))/(len(s1) + len(s2))/2

	def get_sentences_rank(self):
		sentences = self.split_content_to_sentences()
		n = len(sentences)
		values = [[0 for x in range(n)] for y in range(n)] #values = np.Zeros(n.n)

		for i in range(n):
			for j in range(n):
				values[i][j] = self.sentences_intersection(sentences[i],sentences[j])

		sentences_dic = {}
		for i in range(n):
			score = 0
			for j in range(n):
				if i == j: continue
				score += values[i][j]
			sentences_dic[self.format_sentence(sentences[i])] = score + self.sentences_intersection(sentences[i], self.tittle)

		return sentences_dic

	def get_summmary(self):
		sentences_dic = self.get_sentences_rank()
		paragrahps = self.split_content_to_paragraphs()
		summary = []
		summary.append(self.tittle.strip())
		summary.append('')

		for p in paragrahps:
			sentence = self.get_best_sentence(p,sentences_dic).strip()
			if sentence: summary.append(sentence)

		return summary
