#!/usr/bin/env python

'''
   Author: Ti-Cheng Chang
   Date: Jun 1, 2018
   Instituion: St Jude Children's Research Hospital
'''
import argparse
import re
import pandas as pd
import os
import collections
from bx.bbi.bigwig_file import BigWigFile

class circosplot(object):
    def __init__(self, link, segment, coverage):
        self.link=link
        self.segment=segment
        self.coverage=coverage
    
        
def karyotype(chr_list=None):
    chr_order = ['chr{}'.format(i) for i in range(1, 22)]
    chr_order.extend(['chrX','chrY'])
    chr_sz={'chr1':{'short':1, 'size': 249250621, 'col':'grey'},
            'chr2':{'short':2, 'size': 243199373, 'col':'black'},
            'chr3':{'short':3, 'size': 198022430, 'col':'grey'},
            'chr4':{'short':4, 'size': 191154276, 'col':'dark2-8-qual-1'},
            'chr5':{'short':5, 'size': 180915260, 'col':'grey'},
            'chr6':{'short':6, 'size': 171115067, 'col':'black'},
            'chr7':{'short':7, 'size': 159138663, 'col':'set1-9-qual-5'},
            'chr8':{'short':8, 'size': 146364022, 'col':'set1-9-qual-2'},
            'chr9':{'short':9, 'size': 141213431, 'col':'grey'},
            'chr10':{'short':10,'size':135534747, 'col':'black'},
            'chr11':{'short':11,'size':135006516, 'col':'grey'},
            'chr12':{'short':12,'size':133851895, 'col':'set1-9-qual-2'},
            'chr13':{'short':13,'size':115169878, 'col':'grey'},
            'chr14':{'short':14,'size':107349540, 'col':'black'},
            'chr15':{'short':15,'size':102531392, 'col':'grey'},
            'chr16':{'short':16,'size':90354753,  'col':'black'},
            'chr17':{'short':17,'size':81195210, 'col':'grey'},
            'chr18':{'short':18,'size':78077248, 'col':'black'},
            'chr19':{'short':19,'size':59128983, 'col':'grey'},
            'chr20':{'short':20,'size':63025520, 'col':'black'},
            'chr21':{'short':21,'size':48129895, 'col':'grey'},
            'chr22':{'short':22,'size':51304566, 'col':'black'},
            'chrX':{'short':'X','size':155270560, 'col':'grey'},
            'chrY':{'short':'Y','size':59373566, 'col':'black'}}
    chr_sz=collections.OrderedDict((k, chr_sz[k]) for k in chr_order)
    k=''
    chr_list=chr_sz.keys() if not chr_list else chr_list
    for chr in chr_list:
        idio=' '.join(map(str,['chr', '-', chr, chr_sz[chr]['short'], 0, chr_sz[chr]['size'], chr_sz[chr]['col']]))+'\n'
        k=k+idio
    return k

def circos_conf(args, spans=None, breaks=None, show_tick='yes', cov_max=500, show_link_end=False):
    sn=args.sample_name
    cov_max=args.cov_max
    fn_karyotype =args.output_folder + '/' + args.output_pre + '.karyotype'
    fn_genelabel =args.output_folder + '/' + args.output_pre + '.gene_label.txt'
    fn_geneseg   =args.output_folder + '/' + args.output_pre + '.geneseg.txt' 
    fn_segment   =args.output_folder + '/' + args.output_pre + '.segment.txt'
    fn_highlight =args.output_folder + '/' + args.output_pre + '.highlight.txt'
    fn_link      =args.output_folder + '/' + args.output_pre + '.link.txt'
    fn_linkend   =args.output_folder + '/' + args.output_pre + '.linkend.txt'
    fn_coverage3 =args.output_folder + '/' + args.output_pre + '.coverage3.txt'
    fn_coverage2 =args.output_folder + '/' + args.output_pre + '.coverage2.txt'
    fn_coverage1 =args.output_folder + '/' + args.output_pre + '.coverage1.txt'

    fn_png       =args.output_pre + '.circos.png'
    svg_out      ='yes'  
    fn           =args.output_folder + '/' + sn +'.circos.conf'
    f = open(fn, 'w')
   

    ### restrict chr to specific regions
    regions=''
    chr_display='yes'
    if spans is not None:
        chr_display='no'
        regions=[]
        for idx, row in spans.iterrows():
            item=row['chr']+':'+str(row['start'])+'-'+str(row['end'])
            regions.append(item)
        regions=';'.join(regions) 
        print regions        
 
    ### suppress regions on chromosomes
    brk_regions=''
    if breaks is not None and breaks.shape[0] > 0:
        brk_regions=[]
        for idx, row in breaks.iterrows():
            item=row['chr']+':'+str(row['start'])+'-'+str(row['end'])
            brk_regions.append(item)
        brk_regions=';'.join(brk_regions)
        print  brk_regions
    ### check if to draw link end arrows
    linkend='\n'
    if args.add_link_end:
        linkend='\n'.join([
            '<plot>',
            'type       =scatter',
            'file       ='+fn_linkend,
            'glyph      = triangle',
            'glyph_size = 16p',
            'min        = 0',
            'max        = 1',
            'r0         = 0.59r',
            'r1         = 0.59r',
            #'fill_color = set1-9-qual-2',
            '</plot>'])



    c='\n'.join([
    '<<include etc/housekeeping.conf>>',
    '<<include etc/colors_fonts_patterns.conf>>',
    'show_ticks*=' + show_tick,
    'show_tick_labels    = yes',
    'svg='+svg_out,
    'karyotype='+ fn_karyotype,
    'chromosomes_display_default ='+chr_display,
    'chromosomes=' + regions,
    'chromosomes_breaks=' + brk_regions,
    #'chromosomes_units           = 1000000', ### for define some breaks
 
    '<ticks>', 
        'radius               = dims(ideogram,radius_outer)',
        'label_offset         = 5p',
        'orientation          = out',
        'label_multiplier     = 1e-6',
        '<tick>',
            #'#chromosomes    = -hs2',
            'spacing        = 500000',
            #'spacing        = 50000',
            'size           = 8p',
            'thickness      = 4p',
            'color          = black',
            'show_label     = yes',
            'label_size     = 40p',
            'label_color    = black',
            'label_offset   = 3p',
            'format         = %.1f',
        '</tick>',
        '<tick>',
            #'#chromosomes    = -hs2',
            'spacing        = 50000',
            #'spacing        = 5000',
            'size           = 4p',
            'thickness      = 2p',
            'color          = dgrey',
            'show_label     = no',
            'label_size     = 40p',
            'label_color    = dgrey',
            'label_offset   = 3p',
            'format         = %.1f',
        '</tick>',

    '</ticks>',

    '<ideogram>',
        'radius           = 0.70r',
        'thickness        = 70p',
        'fill             = yes',
        'fill_color       = black',
        'stroke_thickness = 2',
        'stroke_color     = black',

        'show_label       = yes',
        'label_font       = bold',
        'label_color      = white',
        'label_radius     = ((dims(ideogram,radius_inner) + dims(ideogram,radius_outer))/2)-18',
        'label_with_tag   = yes',
        'label_case       = upper',
        'label_parallel   = yes',
        'label_size       = 40',

        'show_bands            = no',
        'fill_bands            = no',
        'band_stroke_thickness = 0',
        'band_stroke_color     = white',
        'band_transparency     = 1',

        '<spacing>',

            'default = 0.05r',
            'break   = 0.02r',

            'axis_break_at_edge = yes',
            'axis_break         = yes',
            'axis_break_style   = 2',

            '<break_style 1>',
                'stroke_color = black',
                'fill_color   = blue',
                'thickness    = 0.25r',
                'stroke_thickness = 2p',
            '</break>',

            '<break_style 2>',
                'stroke_color     = black',
                'stroke_thickness = 5p',
                'thickness        = 2r',
            '</break>',
            
            '<pairwise chr7>',
                'spacing = 0.15r',
            '</pairwise>',

            '<pairwise chr7 chr12>',
                'spacing = 0.05r',
            '</pairwise>',

        '</spacing>',
    '</ideogram>',

    ### output
    '<image>',
    'dir         =' + args.output_folder,
    'file        =' + fn_png,
    'radius      = 1200p',
    'background  = white',
    'angle_offset= -90',
    #'angle_offset= 10',
    'png         = yes',
    '24bit       = yes',
    'auto_alpha_colors = no',
    'auto_alpha_steps  = 10',
    '</image>',

    '<plots>',
    ### highlight band
    #'<plot>',
    #'type = highlight',
    #'file = ' + fn_segment,
    #'r0   = dims(ideogram,radius_inner)',
    #'r1   = dims(ideogram,radius_outer)',
    #'stroke_thickness=4',
    #'</plot>',
    
    ### gene/segment labels
    #'<plot>',
    #    'type        = text',
    #    'color       = black',
    #    'file        = ' + fn_genelabel,
    
    #    #'# inside circle',
    #    #'# r0 = 0.4r',
    #    #'# r1 = 0.8r',
    
    #    #'# on tick scale',
    #    'r0 = 1r',
    #    'r1 = 1r+300p',
     
    #    'show_links  = yes',
    #    'link_dims   = 0p,0p,50p,0p,10p',
    #    '#link_dims      = 4p,4p,8p,4p,4p',
    #    'link_thickness = 2p',
    #    'link_color     = black',
    
    #    'label_size   = 48p',
    #    'label_font   = condensed',
    
    #    'label_snuggle        = yes',
    #    'max_snuggle_distance  = 1.2r',
    #    'snuggle_tolerance     = 0.25r',
    #    'snuggle_sampling      = 0',
    
    #    'padding  = 0p',
    #    'rpadding = 0p',
    
    #'</plot>',
    
    ### segment
    '<plot>',
        'type            = tile',
        'file            = ' + fn_segment,
        'r1              =0.69r',
        'r0              =0.60r',
        'orientation     = in',
        'layers          = 2',
        'margin          = 0.02u',
        'thickness       = 25',
        'padding         = 8',
        'stroke_thickness= 1',
        'stroke_color    = black',
        'layers_overflow = collapse',
        'layers_overflow_color = red',
        '<backgrounds>',
            '<background>',
                'color = vlgrey',
            '</background>',
        '</backgrounds>',
    '</plot>',
   
    ### gene segment
    #'<plot>',
    #    'type            = tile',
    #    'file            = ' + fn_geneseg,
    #    'r1              =0.99r',
    #    'r0              =0.90r',
    #    'orientation     = in',
    #    'layers          = 1',
    #    'margin          = 0.02u',
    #    'thickness       = 60',
    #    'padding         = 8',
    #    'stroke_thickness= 0',
    #    'stroke_color    = black',
    #    'fill_color      = dgrey',
    #    'layers_overflow = grow',
    #    #'layers_overflow_color = black',
    #    '<backgrounds>',
    #        '<background>',
    #            'color = vlgrey',
    #        '</background>',
    #    '</backgrounds>',
    #'</plot>',



    ### linkend
    #'<plot>',
    #    'type       =scatter',
    #    'file       ='+fn_linkend,
    #    'glyph      = triangle',
    #    'glyph_size = 16p',
    #    'min        = 0',
    #    'max        = 1',
    #    'r0         = 0.59r',
    #    'r1         = 0.59r',
    #    #'fill_color = set1-9-qual-2',
    #'</plot>',
    linkend,

    ### coverage hist
    '<plot>',
        'type = histogram',
        'file = ' + fn_coverage3,
        'r1 = 0.79r',
        'r0 = 0.70r',
        'min= 0',
        'max= '+str(cov_max),
        'orientation = out',
        'fill_color  =' + args.coverage3_trackc,
        '<backgrounds>',
            '<background>',
            '    color = vvlgrey',
            '</background>',
        '</backgrounds>',
    '</plot>',
    '<plot>',
        'type = histogram',
        'file = ' + fn_coverage2,
        'r1 = 0.89r',
        'r0 = 0.80r',
        'min= 0',
        'max= '+str(cov_max),
        'orientation = out',
        'fill_color  =' + args.coverage2_trackc,
        '<backgrounds>',
            '<background>',
            '    color = vvlgrey',
            '</background>',
        '</backgrounds>',
    '</plot>',
    '<plot>',
        'type = histogram',
        'file = ' + fn_coverage1,
        'r1 = 0.99r',
        'r0 = 0.90r',
        'min= 0',
        'max= '+str(cov_max),
        'orientation = out',
        'fill_color  = ' + args.coverage1_trackc,
        '<backgrounds>',
            '<background>',
            '    color = vvlgrey',
            '</background>',
        '</backgrounds>',
    '</plot>',
    '</plots>',
   
    ### links
    
    '<links>',
        'z                   =0',
        'radius              =0.59r',
        'crest               =0.5',
        'bezier_radius       =0.15r', ### srength of the curve
        #'bezier_radius_purity=0.75',
        '<link>',
            'z                    =0',
            #'color                =set1-9-qual-7',
            'thickness            =4',
            'file                 ='+fn_link,
            #'bezier_radius_purity = 0.2',
            #'crest                = 0.5',
            '<rules>',
                '<rule>',
                    'condition  = var(type) eq \"dm3\"',
                    'bezier_radius       =0.18r',
                '</rule>',
                '<rule>',
                    'condition  = var(type) eq \"dm2\"',
                    'bezier_radius       =0.16r',
                '</rule>',
                '<rule>',
                    'condition  = var(type) eq \"dm1\"',
                    'bezier_radius       =0.14r',
                '</rule>',
                '<rule>',
                    'condition  = var(type) eq \"dm5\"',
                    'bezier_radius       =0.12r',
                '</rule>',
                '<rule>',
                    'condition  = var(type) eq \"dm4\"',
                    'bezier_radius       =0.10r',
                '</rule>',
                '<rule>',
                    'condition  = var(type) eq \"softclip\"',
                    'bezier_radius       =0.18r',
                '</rule>',
                '<rule>',
                    'condition  = var(type) eq \"discordant\"',
                    'bezier_radius       =0.16r',
                '</rule>',
                '<rule>',
                    'condition  = var(type) eq \"bridge\"',
                    'bezier_radius       =0.14r',
                '</rule>',

            '</rules>',
        '</link>',  
        
    '</links>',
    

    ])
    f.write(c);
    f.close();
    return fn, fn_png

def indata_prep(fn, type):
    df=None
    if type=='link':
        df=pd.read_table(fn, header=None)
        df.columns = ['chr_s', 'start_s', 'end_s', 'chr_e', 'start_e', 'end_e', 'type']
        print("[link] file headers: %s" %list(df))
    elif type=='segment':
        df=pd.read_table(fn, header=None)
        if df.shape[1]==6:
            df.columns = ['chr', 'start', 'end', 'name', 'name1', 'logR']
        elif df.shape[1]==4:
            df.columns = ['chr', 'start', 'end', 'logR']
            df['name']=df.index
        print("[segment] file headers: %s" % list(df))
    elif type=='geneseg':
        df=pd.read_table(fn, header=None)
        df.columns = ['chr', 'start', 'end', 'name']
        print("[geneseg] file headers: %s" % list(df))
    elif type=='coverage':
        print("Input file headers: %s" % fn)
    else:
        print "Unknown datatype"
    return df


def link_color_set(set):
    set1=['dark2-8-qual-1','dark2-8-qual-2', 'dark2-8-qual-3', 'dark2-8-qual-4', 'dark2-8-qual-5']
    set2=['set1-9-qual-1','set1-9-qual-2', 'set1-9-qual-3', 'set1-9-qual-4', 'set1-9-qual-5']
    set3=['set2-8-qual-1','set2-8-qual-2','set2-8-qual-4']
    if set == 1:
        return set1
    elif set == 2:
        return set2 
    elif set == 3:
        return set3
    else:
        return set1


def datafile(args, extend=100000, break_dist=5000000):
    karyotype_filename =args.output_folder + '/' + args.output_pre + '.karyotype'
    genelabel_filename =args.output_folder + '/' + args.output_pre + '.gene_label.txt'
    segment_filename   =args.output_folder + '/' + args.output_pre + '.segment.txt'
    geneseg_filename =args.output_folder + '/' + args.output_pre + '.geneseg.txt'
    highlight_filename =args.output_folder + '/' + args.output_pre + '.highlight.txt'
    link_filename      =args.output_folder + '/' + args.output_pre + '.link.txt'
    linkend_filename   =args.output_folder + '/' + args.output_pre + '.linkend.txt'
    coverage3_filename  =args.output_folder + '/' + args.output_pre + '.coverage3.txt'
    coverage2_filename  =args.output_folder + '/' + args.output_pre + '.coverage2.txt'
    coverage1_filename  =args.output_folder + '/' + args.output_pre + '.coverage1.txt'

    linkdf=indata_prep(args.link_file, 'link') if args.link_file else None
    segmentdf=indata_prep(args.segment_file, 'segment') if args.segment_file else None 
    genesegdf=indata_prep(args.genesegment_file, 'geneseg') if args.segment_file else None   
    extraseg =indata_prep(args.extra_segment_file, 'segment') if args.segment_file else None 

    segmentdf.sort_values(by=['chr','start'], inplace=True)
    segmentdf.reset_index(drop=True, inplace=True)  
  
    ### add extra seg for karyotype if present
    allsegs  =None
    if extraseg is not None:
        frames=[segmentdf, extraseg]
        allsegs=pd.concat(frames)
    else:
        allsegs=segmentdf
   
    chrs=allsegs.chr.unique().tolist()
    k=karyotype(chrs) + '\n'
    span=allsegs.groupby('chr').agg({'start':'min','end':'max'})[['start','end']].reset_index()
    allsegs.sort_values(by=['chr','start'], inplace=True)
    allsegs.reset_index(drop=True, inplace=True)
    ### break segment with long spanning distance
    breaks=[]
    for idx, row in allsegs.iterrows():
        if idx+1 < allsegs.shape[0]:
            #print segmentdf.ix[idx,'chr'], segmentdf.ix[idx,'end'], segmentdf.ix[idx+1,'chr'], segmentdf.ix[idx+1,'start']
            if allsegs.ix[idx,'chr'] == allsegs.ix[idx+1,'chr']:
                dist=int(allsegs.ix[idx+1,'start'])-int(allsegs.ix[idx,'end'])
                if dist >= break_dist:
                    interval = {'chr':allsegs.ix[idx,'chr'], 'start':int(allsegs.ix[idx,'end'])+extend, 'end': int(allsegs.ix[idx+1,'start'])-extend}
            	    breaks.append(interval)
    breaks=pd.DataFrame(breaks)
    span['start']=span['start'].apply(lambda x:x-extend)
    span['end']=span['end'].apply(lambda x:x+extend)
    ### karyotype
    f = open(karyotype_filename, 'w')
    f.write(k); f.close()

    ### segment ... use gene band
    f1= open(genelabel_filename, 'w')
    f2= open(segment_filename, 'w')
    lbcol='black'
    lncol='black'
    for idx, row in segmentdf.iterrows():
        label=' '.join(map(str,[ row['chr'], row['start'], row['end'], row['name'], 'color='+lbcol+',link_color='+lncol])) + '\n' 
        segment=' '.join(map(str,[ row['chr'], row['start'], row['end']]))+'\n'
        f1.write(label)
        f2.write(segment)
    f1.close()
    f2.close()

    ### gene segment 
    f7=open(geneseg_filename, 'w')
    gcol='grey'
    for idx, row in genesegdf.iterrows():
        if row['name']=='EGFR':
            gcol='Set2-8-qual-2'
        elif row['name']=='MYC':
            gcol='Set2-8-qual-3'
        elif row['name']=='CDK6':
            gcol='Set2-8-qual-4'
        segment=' '.join(map(str,[ row['chr'], row['start'], row['end'], 'color='+gcol]))+'\n' 
        f7.write(segment)
    f7.close()


    ### link 
    f3= open(link_filename, 'w')
    f4= open(linkend_filename, 'w')
    color='set1-9-qual-7'
    link_colorset=link_color_set(args.link_color_set)
    for idx, row in linkdf.iterrows():
        #[link] file headers: ['chr_s', 'start_s', 'end_s', 'chr_e', 'start_e', 'end_e', 'type']
        linkn='link'+str(idx)
        if row['type']=='dm1':
            color=link_colorset[0]
        elif row['type']=='dm2':
            color=link_colorset[1]
        elif row['type']=='dm3':
            color=link_colorset[2]
        elif row['type']=='dm4':
            color=link_colorset[3]
        elif row['type']=='dm5':
            color=link_colorset[4]
        elif row['type']=='softclip':
            color=link_colorset[0] # green
        elif row['type']=='discordant':
            color=link_colorset[1] # orange
        elif row['type']=='bridge':
            color=link_colorset[2] # pink
        
        links=' '.join(map(str,[linkn, row['chr_s'], row['start_s'], row['end_s'], ','.join(['color='+color,'type='+row['type']])]))
        linke=' '.join(map(str,[linkn, row['chr_e'], row['start_e'], row['end_e'], ','.join(['color='+color,'type='+row['type']])]))
        linkend=' '.join(map(str,[row['chr_e'], row['start_e'], row['end_e'], 0, 'fill_color='+color]))
        f3.write(links+'\n')
        f3.write(linke+'\n')
        f4.write(linkend+'\n')
    f3.close()
    f4.close()
    
    ### coverage
    w=args.coverage_window_size
    f5=open(coverage3_filename, 'w')
    if args.coverage3_file: 
        bw = BigWigFile(open(args.coverage3_file))
        for idx, row in span.iterrows():
            size=int(row['end'])-int(row['start'])
            winn=size/float(w)
            print "windows %s" % str(winn)
            for pos in range(int(row['start']), int(row['end']), w):
                wcov=bw.query(row['chr'], pos, pos+w, 1)
                means = [ x['mean'] for x in wcov ]
                out=' '.join(map(str,[ row['chr'], pos, pos+w, means[0]]))
                f5.write(out+'\n')
    f5.close()
    
    f8=open(coverage2_filename, 'w')
    if args.coverage2_file:
        bw = BigWigFile(open(args.coverage2_file))
        for idx, row in span.iterrows():
            size=int(row['end'])-int(row['start'])
            winn=size/float(w)
            print "windows %s" % str(winn)
            for pos in range(int(row['start']), int(row['end']), w):
                wcov=bw.query(row['chr'], pos, pos+w, 1)
                means = [ x['mean'] for x in wcov ]
                out=' '.join(map(str,[ row['chr'], pos, pos+w, means[0]]))
                f8.write(out+'\n')
    f8.close()

 

    f6=open(coverage1_filename, 'w')
    if args.coverage1_file:
        bw = BigWigFile(open(args.coverage1_file))
        for idx, row in span.iterrows():
            size=int(row['end'])-int(row['start'])
            winn=size/float(w)
            print "windows %s" % str(winn)
            for pos in range(int(row['start']), int(row['end']), w):
                wcov=bw.query(row['chr'], pos, pos+w, 1)
                means = [ x['mean'] for x in wcov ]
                out=' '.join(map(str,[ row['chr'], pos, pos+w, means[0]]))
                f6.write(out+'\n')
    f6.close()


    return span, breaks

def run_circos(conf, label, png):
    try:
         ### load circos
         os.system("module load circos/0.69")
         print("Circos 0.69 loaded...")
         
         ### run circos
         os.system("circos -conf " + conf +" -noparanoid")
         print("Circos done")

    except ValueError:
        print("Errors ... exit")
    

def run(args):
    #print("Input: %s" % args.input)
    sn=args.sample_name
    print("Sample:%s" % sn)

    if args.output_pre is None:
        args.output_pre=sn

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    span, breaks=datafile(args)
    fn_c, fn_p = circos_conf(args, spans=span, breaks=breaks, show_tick='yes')
    run_circos(fn_c, sn, args.output_folder + '/' + fn_p)

def main():
    parser = argparse.ArgumentParser(description='Convert mutation file to circos format', \
                                     epilog     ='''This script will plot the connection between CNV segments, connection of segments in episome and the coverage of the defined regions using Circos. 
                                                  Circos should be installed before running the script''')
    parser.add_argument('-link', '--link_file', help='Link file input', required=False)
    parser.add_argument('-link_color', '--link_color_set', help='Link color set', default=1, type=int)
    parser.add_argument('-add_link_end', '--add_link_end', help='Add arrows to link ends', action='store_true')
    parser.add_argument('-segment', '--segment_file', help='Segment file input', required=False)
    parser.add_argument('-extraseg', '--extra_segment_file', help='Additional segment file for expanding karyotype', required=False)
    parser.add_argument('-gene', '--genesegment_file', help='Gene segment file input', required=False)
    parser.add_argument('-coverage1', '--coverage1_file', help='Sample 1 coverage file input', required=False)
    parser.add_argument('-coverage1_c', '--coverage1_trackc', help='Sample 1 coverage track color', default='green')
    parser.add_argument('-coverage2', '--coverage2_file', help='Sample 2 coverage file input', required=False)
    parser.add_argument('-coverage2_c', '--coverage2_trackc', help='Sample 2 coverage track color', default='153,0,0')
    parser.add_argument('-coverage3', '--coverage3_file', help='Sample 3 sample coverage file input', required=False)
    parser.add_argument('-coverage3_c', '--coverage3_trackc', help='Sample 3 coverage track color', default='0,0,178')
    parser.add_argument('-sn', '--sample_name', help='Sample name', required=True)
    parser.add_argument('-p', '--output_pre', help='circos config output prefix')
    parser.add_argument('-d', '--output_folder', help='circos plot output folder', default='./')
    parser.add_argument('-z', '--coverage_window_size', help='window size for calculating coverage average', default=10000, type=int)
    parser.add_argument('-covmax', '--cov_max', help='Upper bound of coverage', default=200, type=int)
    args=parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()

