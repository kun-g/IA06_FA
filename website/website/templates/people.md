# {{ name }}
* 维基百科地址：[{{ name }}]({{ wiki_url }})
* 下一步建议：
  * 详细阅读Wikipedia
{% if Turing_Award %}  * 阅读图灵奖委员会写的小传: [{{ name }}]({{ Turing_Award.url }})
  * 查看ACM DL页面: [{{ name }}]({{ Turing_Award.dl_link }}) {% endif %}

## 时间
### 生卒年月
* {{ Born.day }} - {% if Died %} {{ Died.day }} {% else %} ? {% endif %}
### 求学经历
{% for e in Alma_mater %}* [{{ e.title }}]({{ e.url }})
{% endfor %}

## 空间
### 学术领域
{% for e in Fields %}* [{{ e.title }}]({{ e.url }})
{% endfor %}

### 获奖情况
{% for e in Awards %}* {{ e.title }} ({{ e.year }})
{% endfor %}

{% if Turing_Award %}
#### 图灵奖
* 页面: [{{ name }}]({{ Turing_Award.url }})
* 获奖原因：
> {{ Turing_Award.citation }}
{% if Turing_Award.award_video %}* [视频]({{ Turing_Award.award_video}}) {% endif %}
{% if Turing_Award.award_lecture %}* [Lecture]({{ Turing_Award.award_lecture }}) {% endif %}
{% endif %}

### 所属机构
{% for e in Institutions %}* [{{ e.title }}]({{ e.url }})
{% endfor %}

## 变量
### 主要成就
{% for e in Known_for %}* [{{ e.title }}]({{ e.url }})
{% endfor %}

### 合作关系
### 师承关系
* 可以去以下网站查找师承关系
  * [Mathematics Genealogy Project](https://genealogy.math.ndsu.nodak.edu/)
  * [academictree](https://academictree.org/)
  * [AceMap](https://www.acemap.info/)
{% if Doctoral_advisor  %}#### 老师
{% for e in Doctoral_advisor %}* [{{ e.title }}]({{ e.url }})
{% endfor %}
{% endif %}
{% if Doctoral_students %}#### 学生
{% for e in Doctoral_students %}* [{{ e.title }}]({{ e.url }})
{% endfor %}
{% endif %}